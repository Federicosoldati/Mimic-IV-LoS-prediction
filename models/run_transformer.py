from eICU_preprocessing.split_train_test import create_folder
from torch.optim import Adam
from models.transformer_model import Transformer
from trixi.util import Config
import argparse
from models.experiment_template import ExperimentTemplate


class BaselineTransformer(ExperimentTemplate):
    def setup(self):
        self.setup_template()
        self.model = Transformer(config=self.config,
                                 F=self.train_datareader.F,
                                 D=self.train_datareader.D,
                                 no_flat_features=self.train_datareader.no_flat_features).to(device=self.device)
        self.elog.print(self.model)
        self.optimiser = Adam(self.model.parameters(), lr=self.config.learning_rate, weight_decay=self.config.L2_regularisation)
        return

if __name__=='__main__':

    # not hyperparams
    parser = argparse.ArgumentParser()
    parser.add_argument('-disable_cuda', action='store_true')
    parser.add_argument('--intermediate_reporting', action='store_true')
    parser.add_argument('--exp_name', default='Transformer', type=str)
    parser.add_argument('--mode', default='train', type=str)
    parser.add_argument('--n_epochs', default=30, type=int)
    parser.add_argument('--batch_size_test', default=128, type=int)
    parser.add_argument('--resume_last', action='store_true')
    parser.add_argument('-shuffle_train', action='store_true')

    # hyperparams
    parser.add_argument('--batch_size', default=128, type=int)
    parser.add_argument('--L2_regularisation', default=0, type=float)
    parser.add_argument('--trans_dropout_rate', default=0.3, type=float)
    parser.add_argument('--main_dropout_rate', default=0.45, type=float)
    parser.add_argument('--learning_rate', default=0.001, type=float)
    parser.add_argument('--d_model', default=128, type=int)
    parser.add_argument('--n_layers', default=4, type=int)
    parser.add_argument('--n_heads', default=8, type=int)
    parser.add_argument('--feedforward_size', default=32, type=int)
    parser.add_argument('--diagnosis_size', default=64, type=int)
    parser.add_argument('--loss', default='msle', type=str, help='can either be msle or mse')
    parser.add_argument('--batchnorm', default='none', type=str)
    parser.add_argument('--last_linear_size', default=17, type=int)
    parser.add_argument('-sum_losses', action='store_true')
    parser.add_argument('-labs_only', action='store_true')
    parser.add_argument('-no_mask', action='store_true')
    parser.add_argument('-no_diag', action='store_true')
    parser.add_argument('-no_labs', action='store_true')
    parser.add_argument('-no_exp', action='store_true')
    args = parser.parse_args()

    # prepare config dictionary, add all arguments from args
    c = Config()
    for arg in vars(args):
        c[arg] = getattr(args, arg)

    log_folder_path = create_folder('models/experiments', c.exp_name)
    baseline_transformer = BaselineTransformer(config=c,
                                               n_epochs=c.n_epochs,
                                               name=c.exp_name,
                                               base_dir=log_folder_path,
                                               explogger_kwargs={'folder_format': '%Y-%m-%d_%H%M%S'})
    if c.mode == 'train':
        baseline_transformer.run()
    if c.mode == 'test':
        baseline_transformer.run_test()