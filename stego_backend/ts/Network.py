import math
import torch
import torch.nn as nn
import torch.nn.functional as F

class FS(nn.Module):
    def __init__(self, args):
        super(FS, self).__init__()
        self.args = args
        self.bert = args.model
        self.fc1 = nn.Linear(768, 2)
        self.softmax = nn.Softmax(dim=-1)
        self.dropout = nn.Dropout(0.5)

        for param in self.bert.parameters():
            param.requires_grad = True

    def forward(self, x):
        context, mask = x[0], x[2]
        _, outputs = self.bert(context, attention_mask=mask)
        # logits = self.dropout(outputs)
        # outputs = self.fc1(outputs)
        outputs = self.softmax(outputs)
        return outputs


# -------------------------------- BertCNN -------------------------------
class TextCNN(nn.Module):
    def __init__(self, args):
        super(TextCNN, self).__init__()
        self.args = args
        self.hidden_size = args.hidden_size
        self.n_class = 2
        self.filter_sizes = [2, 3, 4]
        # self.filter_sizes = [2, 2, 2]
        self.num_filters = 3
        self.encode_layer = args.encode_layer
        self.num_filter_total = self.num_filters * len(self.filter_sizes)
        self.Weight = nn.Linear(self.num_filter_total+768, self.n_class, bias=False)
        # self.Weight = nn.Linear(24, self.n_class, bias=False)
        self.bias = nn.Parameter(torch.ones([self.n_class]))
        self.filter_list = nn.ModuleList([nn.Conv2d(1, self.num_filters, kernel_size=(size, self.hidden_size)) for size in self.filter_sizes])

    def forward(self, x):
        # x: [batch_size, seq_len, hidden_size]

        # -------------- CLS平均和最后一层其余接CNN进行cat --------------
        cls_embedding = x[:, 0, :]
        x = x[:, 1:, :]
        x = x.unsqueeze(1)  # [batch_size, channel=1, seq_len, hidden_size]
        pooled_outputs = []
        for i, conv in enumerate(self.filter_list):
            h = F.relu(conv(x))  # [batch_size, channel=1, seq_len - kernel_size + 1, 1]
            # maxpooling = nn.MaxPool2d(kernel_size=(self.encode_layer - self.filter_sizes[i] + 1, 1))
            maxpooling = nn.MaxPool2d(kernel_size=(31 - self.filter_sizes[i] + 1, 1))
            # maxpooling: [batch_size, channel=3, weight, h]
            h_maxpooling = maxpooling(h)
            pooled = h_maxpooling.permute(0, 3, 2, 1)  # [batch_size, h=1, w=1, channel=3]
            pooled_outputs.append(pooled)

        h_pool = torch.cat(pooled_outputs, dim=1)  # [bs, h=1, w=1, channel=3 * 3]
        h_pool_flat = torch.reshape(h_pool, [-1, self.num_filter_total])
        h_pool_flat = torch.cat((h_pool_flat, cls_embedding), dim=1)
        output = self.Weight(h_pool_flat) + self.bias  # [bs, n_class]
        return output


class Bert_CNN(nn.Module):
    def __init__(self, args):
        super(Bert_CNN, self).__init__()
        self.args = args
        self.bert = args.model
        self.textcnn = TextCNN(args=args)
        self.fc1 = nn.Linear(768, 2)
        unfreeze_layers = ['layer.10', 'layer.11', 'bert.pooler', 'out.']
        for name, param in self.bert.named_parameters():
            print(name, param.size())
        for param in self.bert.parameters():
            param.requires_grad = False
            for ele in unfreeze_layers:
                if ele in name:
                    param.requires_grad = True
                    break

    def forward(self, x):
        """
        context: [batch_size, seq_len],                 Tensor,  每个单词序列化，并补长
        outputs[0]: [batch_size, seq_len, hidden_size], Tensor,  最后一层encoder的输出
        outputs[1]: [batch_size, hidden_size],          Tensor,  pooler的输出，接linear
        outputs[2]: 13 * [batch_size, seq_len, hidden], tuple,   (0位置是embedding层的输出)
        hidden_states == outputs[2]
        """
        context = x[0]
        mask = x[2]
        outputs = self.bert(context, attention_mask=mask, output_hidden_states=True)

        # -------------- CLS接TextCNN --------------
        # hidden_states = outputs[2]
        # cls_embedding = hidden_states[0][:, 0, :].unsqueeze(1)
        # for i in range(1, 13):
        #     cls_embedding = torch.cat((cls_embedding, hidden_states[i][:, 0, :].unsqueeze(1)), dim=1)  # [batch_size, encoder_layer(12), hidden_size]
        # logits = self.textcnn(cls_embedding)

        # -------------- 每层CLS取平均 --------------
        # cls_embedding = torch.mean(cls_embedding, dim=1)
        # logits = self.fc1(cls_embedding)

        # -------------- 最后一层接CNN --------------
        # bertoutput = outputs[2][-1]
        # logits = self.textcnn(bertoutput)

        # -------------- CLS平均和最后一层其余的cat接CNN --------------
        hidden_states = outputs[2]
        cls_embedding = hidden_states[0][:, 0, :].unsqueeze(1)
        for i in range(1, 13):
            cls_embedding = torch.cat((cls_embedding, hidden_states[i][:, 0, :].unsqueeze(1)), dim=1)  # [batch_size, encoder_layer(12), hidden_size]
        cls_embedding = torch.mean(cls_embedding, dim=1)
        cls_embedding = cls_embedding.unsqueeze(1)
        bertoutput = outputs[2][-1]
        # bertoutput = bertoutput[:, 1:, :]
        wordoutputs = torch.cat((cls_embedding, bertoutput), dim=1)
        logits = self.textcnn(wordoutputs)

        # -------------- 直接接linear --------------
        # logits = self.fc1(outputs[1])
        return logits


# -------------------------------- Bert -------------------------------
class MyBert(nn.Module):
    def __init__(self, args):
        super(MyBert, self).__init__()
        self.args = args
        self.bert = args.model
        # self.fc1 = nn.Linear(1024, 2)
        self.fc1 = nn.Linear(768, 2)
        # self.fc1 = nn.Linear(1024, 11)
        self.dropout = nn.Dropout(args.dropout)
        for param in self.bert.parameters():
            param.requires_grad = True

        # for param in self.bert.parameters():
        #     param.requires_grad = False

            # 解冻最后两层
        # for param in self.bert.layer[-2:].parameters():
        #     param.requires_grad = True

    def forward(self, x):
        context, mask = x['input_ids'], x['attention_mask']

        # -------------- bert --------------
        outputs = self.bert(context, attention_mask=mask)
        hidden_states = outputs.last_hidden_state
        outputs = hidden_states[:, -1, :]
        # -------------- gpt --------------
        # outputs = self.bert(context, attention_mask=mask)
        # outputs = outputs[0]
        # outputs = outputs[:, -1, :]

        outputs = self.fc1(outputs)
        return outputs


# -------------------------------- BertLstmAtten -------------------------------
class Attention(nn.Module):
    def __init__(self, embed_dim, hidden_dim=None, out_dim=None, n_head=1, score_function='dot_product', dropout=0):
        super(Attention, self).__init__()
        if hidden_dim is None:
            hidden_dim = embed_dim // n_head
        if out_dim is None:
            out_dim = embed_dim
        self.embed_dim = embed_dim
        self.hidden_dim = hidden_dim
        self.n_head = n_head
        self.score_function = score_function
        self.w_k = nn.Linear(embed_dim, n_head * hidden_dim)
        self.w_q = nn.Linear(embed_dim, n_head * hidden_dim)
        self.proj = nn.Linear(n_head * hidden_dim, out_dim)
        self.dropout = nn.Dropout(dropout)

        if self.score_function == 'mlp':
            self.weight = nn.Parameter(torch.Tensor(hidden_dim * 2))
        elif self.score_function == 'bi_linear':
            self.weight = nn.Parameter(torch.Tensor(hidden_dim, hidden_dim))
        else:
            self.register_parameter('weight', None)
        self.reset_parameters()

    def reset_parameters(self):
        stdv = 1. / math.sqrt(self.hidden_dim)
        if self.weight is not None:
            self.weight.data.uniform_(-stdv, stdv)

    def forward(self, k, q):
        if len(q.shape) == 2:
            q = torch.unsqueeze(q, dim=1)
        if len(k.shape) == 2:
            k = torch.unsqueeze(k, dim=1)
        mb_size = k.shape[0]
        k_len = k.shape[1]
        q_len = q.shape[1]
        # k: (?, k_len, embed_dim,)
        # q: (?, q_len, embed_dim,)
        # kx: (n_head*?, k_len, hidden_dim)
        # qx: (n_head*?, q_len, hidden_dim)
        # score: (n_head*?, q_len, k_len,)
        # output: (?, q_len, out_dim,)
        kx = self.w_k(k).view(mb_size, k_len, self.n_head, self.hidden_dim)
        kx = kx.permute(2, 0, 1, 3).contiguous().view(-1, k_len, self.hidden_dim)
        qx = self.w_q(q).view(mb_size, q_len, self.n_head, self.hidden_dim)
        qx = qx.permute(2, 0, 1, 3).contiguous().view(-1, q_len, self.hidden_dim)
        if self.score_function == 'dot_product':
            kt = kx.permute(0, 2, 1)
            score = torch.bmm(qx, kt)
        elif self.score_function == 'scaled_dot_product':
            kt = kx.permute(0, 2, 1)
            qkt = torch.bmm(qx, kt)
            score = torch.div(qkt, math.sqrt(self.hidden_dim))
        elif self.score_function == 'mlp':
            kxx = torch.unsqueeze(kx, dim=1).expand(-1, q_len, -1, -1)
            qxx = torch.unsqueeze(qx, dim=2).expand(-1, -1, k_len, -1)
            kq = torch.cat((kxx, qxx), dim=-1)  # (n_head*?, q_len, k_len, hidden_dim*2)
            # kq = torch.unsqueeze(kx, dim=1) + torch.unsqueeze(qx, dim=2)
            score = torch.tanh(torch.matmul(kq, self.weight))
        elif self.score_function == 'bi_linear':
            qw = torch.matmul(qx, self.weight)
            kt = kx.permute(0, 2, 1)
            score = torch.bmm(qw, kt)
        else:
            raise RuntimeError('invalid score_function')
        score = F.softmax(score, dim=-1)
        output = torch.bmm(score, kx)  # (n_head*?, q_len, hidden_dim)
        output = torch.cat(torch.split(output, mb_size, dim=0), dim=-1)  # (?, q_len, n_head*hidden_dim)
        output = self.proj(output)  # (?, q_len, out_dim)
        output = self.dropout(output)
        return output, score


class lstm(nn.Module):
    def __init__(self, input_size, hidden_size, bidirectional=True):
        super(lstm, self).__init__()
        self.input_size = input_size
        if bidirectional:
            self.hidden_size = hidden_size // 2
        else:
            self.hidden_size = hidden_size
        self.bidirectional = bidirectional

        self.LNx = nn.LayerNorm(4 * self.hidden_size)
        self.LNh = nn.LayerNorm(4 * self.hidden_size)
        self.LNc = nn.LayerNorm(self.hidden_size)
        self.Wx = nn.Linear(in_features=self.input_size, out_features=4 * self.hidden_size, bias=True)
        self.Wh = nn.Linear(in_features=self.hidden_size, out_features=4 * self.hidden_size, bias=True)

    def forward(self, x):
        def recurrence(xt, hidden):  # enhanced with layer norm
            # input: input to the current cell
            htm1, ctm1 = hidden
            gates = self.LNx(self.Wx(xt)) + self.LNh(self.Wh(htm1))
            it, ft, gt, ot = gates.chunk(4, 1)
            it = torch.sigmoid(it)
            ft = torch.sigmoid(ft)
            gt = torch.tanh(gt)
            ot = torch.sigmoid(ot)
            ct = (ft * ctm1) + (it * gt)
            ht = ot * torch.tanh(self.LNc(ct))
            return ht, ct

        output = []
        steps = range(x.size(1))
        hidden = self.init_hidden(x.size(0))
        inputs = x.transpose(0, 1)
        for t in steps:
            hidden = recurrence(inputs[t], hidden)
            output.append(hidden[0])
        output = torch.stack(output, 0).transpose(0, 1)
        if self.bidirectional:
            hidden_b = self.init_hidden(x.size(0))
            output_b = []
            for t in steps[::-1]:
                hidden_b = recurrence(inputs[t], hidden_b)
                output_b.append(hidden_b[0])
            output_b = output_b[::-1]
            output_b = torch.stack(output_b, 0).transpose(0, 1)
            output = torch.cat([output, output_b], dim=-1)
        return output

    def init_hidden(self, bs):
        h_0 = torch.zeros(bs, self.hidden_size).cuda()
        c_0 = torch.zeros(bs, self.hidden_size).cuda()
        return h_0, c_0


class TC_base(nn.Module):
    def __init__(self,in_features, hidden_dim,  class_num, dropout_rate,bidirectional):
        super(TC_base, self).__init__()
        self.in_features = in_features
        self.dropout_prob = dropout_rate
        self.num_labels = class_num
        self.hidden_size = 768
        self.bidirectional = bidirectional
        self.dropout = nn.Dropout(self.dropout_prob)
        self.lstm = lstm(
            input_size=self.in_features,
            hidden_size=self.hidden_size,
            bidirectional=True
        )
        self.attn = Attention(
            embed_dim=self.hidden_size,
            hidden_dim=self.hidden_size,
            n_head=1,
            score_function='mlp',
            dropout=self.dropout_prob
        )
        self.classifier = nn.Linear(self.hidden_size, self.num_labels)

    def forward(self, features, input_ids_len):
        output = self.lstm(features)
        output = self.dropout(output)
        scc, scc1 = self.attn(output,output)
        t = input_ids_len.view(input_ids_len.size(0),1)
        scc_sen = torch.sum(scc,dim=2)
        scc_mean = torch.div(torch.sum(scc,dim=1),t)
        logits = self.classifier(scc_mean)
        return logits

    def extra_repr(self) -> str:
        return 'features {}->{},'.format(
            self.in_features, self.class_num
        )


class BertLstm(nn.Module):
    def __init__(self, args):
        super(BertLstm, self).__init__()
        self.args = args
        self.bert = args.model
        self.fc1 = nn.Linear(768, 2)
        self.hidden_size = 768
        self.num_labels = 4
        self.dropout = nn.Dropout(0.1)
        self.bidirectional = True
        self.embed_size = 768
        self.in_features = 768
        self.lstm = lstm(
            input_size=self.in_features,
            hidden_size=self.hidden_size,
            bidirectional=True
        )
        self.attn = Attention(
            embed_dim=self.hidden_size,
            hidden_dim=self.hidden_size,
            n_head=1,
            score_function='mlp',
        )
        self.classifier = nn.Linear(self.hidden_size, self.num_labels)
        for param in self.bert.parameters():
            param.requires_grad = True

    def forward(self, x):
        context, mask = x[0], x[2]
        input_ids_len = torch.sum(context != 0, dim=-1).float()
        outputs = self.bert(context, attention_mask=mask, output_hidden_states=True)
        output = self.lstm(outputs[2][12])
        output = self.dropout(output)
        scc, scc1 = self.attn(output, output)
        t = input_ids_len.view(input_ids_len.size(0), 1)
        scc_mean = torch.div(torch.sum(scc, dim=1), t)
        logits = self.classifier(scc_mean)
        return logits
