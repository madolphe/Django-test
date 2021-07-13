#%% cell 2
import numpy  as np
import matplotlib.pyplot as plt
import stan
import asyncio
asyncio.run(asyncio.sleep(1))

#fname_csv1 = 'accuracy_data.csv'
class CalStan_accuracy():
    def __init__(self,dataframe,ind_corr_resp='corr_resp',ind_total_resp='total_resp',num_chains=4,num_samples=10000):
        self.binomial_code = """
        data {
          int nums;  //total number of participants
          int corr_resp[nums];  //correct response distributions
          int total_resp[nums]; //total trials
        }
        parameters {
          real<lower=0, upper=1> theta[nums]; //correct probability
        }

        model {
          //model
          for (n in 1:nums){
            corr_resp[n] ~ binomial(total_resp[n],theta[n]);
            //the number of correct response depends on the binomial dist.
          }
          
          //priors
          theta[1] ~ uniform(0,1);
        }

        generated quantities{
          real theta_across_obs=0;
          for (n in 1:nums) {
            theta_across_obs = theta_across_obs + theta[n]/nums;
            } 
        }
        """
        #df_read = pd.read_csv(fname_csv1)
        self.binomial_data = {"nums": len(dataframe),
                        "corr_resp":dataframe[ind_corr_resp].tolist(),
                        "total_resp":dataframe[ind_total_resp].tolist()
                        }
        print(self.binomial_data)
        self.posterior = stan.build(self.binomial_code, data=self.binomial_data)
        self.fit = self.posterior.sample(num_chains=num_chains, num_samples=num_samples)
        #corr_resp = self.fit["corr_resp"]  # array with shape (8, 4000)
        self.df_results = self.fit.to_frame()  # pandas `DataFrame, requires pandas
        #plt.hist(df.loc[:,'diff_theta'])
        self.mu_theta = np.mean(self.df_results.loc[:,'theta_across_obs'].values)
        self.ci_min = np.percentile(self.df_results.loc[:,'theta_across_obs'],2.5)
        self.ci_max = np.percentile(self.df_results.loc[:,'theta_across_obs'],97.5)


class CalStan_rt():
    def __init__(self,dataframe,ind_rt='rt',num_chains=4,num_samples=10000):
        self.binomial_code = """
        data {
          int nums;  //total number of participants
          real rt[nums];  //rt distributions
        }
        parameters {
          real<lower=0> mu[nums]; //mean
          real<lower=0> sigma[nums]; //sigma
        }

        model {
          //model
          for (n in 1:nums){
            rt[n] ~ normal(mu[n],sigma[n]);
            //the number of correct response depends on the binomial dist.
          }
          
          //priors
          for (n in 1:nums){
            mu[n] ~ uniform(0,1000);
            sigma[n] ~ uniform(0,1000);
            }
        }

        generated quantities{
          real mu_across_obs=0;
          for (n in 1:nums) { 
            mu_across_obs = mu_across_obs + mu[n]/nums;
            }
        }
        """
        #df_read = pd.read_csv(fname_csv1)
        self.binomial_data = {"nums": len(dataframe),
                        "rt":dataframe.loc[:,ind_rt].tolist(),
                        }
        print(self.binomial_data)
        self.posterior = stan.build(self.binomial_code, data=self.binomial_data)
        self.fit = self.posterior.sample(num_chains=num_chains,num_samples=num_samples)
        #corr_resp = self.fit["corr_resp"]  # array with shape (8, 4000)
        self.df_results = self.fit.to_frame()  # pandas `DataFrame, requires pandas
        #plt.hist(df.loc[:,'diff_theta'])
        self.mu_rt = np.mean(self.df_results.loc[:,'mu_across_obs'].values)
        self.ci_min = np.percentile(self.df_results.loc[:,'mu_across_obs'],2.5)
        self.ci_max = np.percentile(self.df_results.loc[:,'mu_across_obs'],97.5)