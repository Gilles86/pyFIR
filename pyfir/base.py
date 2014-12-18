import numpy as np
import scipy as sp
from scipy import signal
import matplotlib.pyplot as plt
import seaborn as sns

class FIR:

    def __init__(self, signal):
        self.signal = signal


    def fit(self, onsets, TR, method='ols', len_impulse=16,resolution=None, ):
    
        if not resolution:
            resolution = TR

        n_impulses_per_condition = len_impulse / resolution

        X = FIR.make_fir_design_matrix(onsets.values(), len_impulse, resolution, TR, self.signal.shape[0])

        if method not in ['ols']:
            raise NotImplementedError

        if method == 'ols':
            Y = self.signal
            beta = np.linalg.pinv(X.T.dot(X)).dot(X.T).dot(Y)
            Y_ = beta.dot(X.T)
            resid = Y - Y_
            var = np.diag(np.linalg.pinv(X.T.dot(X)).dot(resid.T.dot(resid) / (X.shape[0] - X.shape[1])))
        
        times = np.arange(0, len_impulse, resolution)

        fir_heights = []
        fir_vars = []
        for i, condition in enumerate(onsets.keys()):
            fir_heights.append(beta[i*n_impulses_per_condition:(i+1)*n_impulses_per_condition])
            fir_vars.append(var[i*n_impulses_per_condition:(i+1)*n_impulses_per_condition])      


        return FIRResults(self, onsets.keys(), times, fir_heights, fir_vars,)




    @staticmethod
    def make_fir_design_matrix(onsets, len_impulse, resolution, TR, n_samples):
        import numpy as np
        
        # How many regressors do we need per condition?/How many timepoints
        # Do we use to model the HRF?
        n_fir_regressors_per_condition = len_impulse / resolution
        
        # Number of TRs we use for that
        n_trs_per_trial = int(len_impulse / TR)    
        
        # Create an empty design matrix
        X = np.zeros((n_samples, len(onsets) * n_fir_regressors_per_condition))
        print X.shape

        # iterate over the conditions
        for condition, onsets_conditions in enumerate(onsets):
            
            # Iterate over trials
            for os in onsets_conditions:
                
                # Find out what the last TR is that happens before or exactly
                # at trial onset: t0
                tr0 = np.floor(os / TR)
                
                # Find out how many resolution elements the offset is between
                # the TR0 and the trial onset.
                offset_in_reso_units = np.floor((os - (tr0 * TR)) / resolution)
                
                # Fill the design matrix accordingly
                for tr in np.arange(n_trs_per_trial):
                    column = condition * n_fir_regressors_per_condition + (tr * TR / resolution) + offset_in_reso_units
                    if tr0 + tr < X.shape[0]:
                        X[tr0 + tr, column] = 1
                    
        return X
        



class FIRResults:

    def __init__(self, fitter, conditions, times, beta, var):
        self.fitter = fitter
        self.conditions = conditions
        self.times = times
        self.beta = beta
        self.var = var


    def plot_results(self, colors=None):
        sem = np.sqrt(self.var)

        if not colors:
            colors = dict(zip(self.conditions, sns.color_palette(n_colors=len(self.conditions))))

        for i, condition in enumerate(self.conditions):
            plt.fill_between(self.times, self.beta[i] - sem[i], self.beta[i] + sem[i], alpha=0.2, color=colors[condition])
            plt.plot(self.times, self.beta[i], label=condition, color=colors[condition])

        plt.axhline(0.0, c='k', ls='--')

        plt.legend()



        

