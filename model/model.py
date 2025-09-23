import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

class TowerGNN(torch.nn.Module):
    def __init__(self, num_node_features, hidden_channels):
        super(TowerGNN, self).__init__()
        torch.manual_seed(12345)
        self.conv1 = GCNConv(num_node_features, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.linear = torch.nn.Linear(hidden_channels, 1)

    def forward(self, x, edge_index):
        # 1. Obtain node embeddings
        x = self.conv1(x, edge_index)
        x = x.relu()
        x = self.conv2(x, edge_index)
        x = x.relu()

        # 3. Apply a final linear layer.
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.linear(x)
        
        return torch.sigmoid(x)