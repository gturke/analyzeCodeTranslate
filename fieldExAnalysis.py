import pandas as pd
import statsmodels.api as sm

# Arguments taken by Chris Kennedy's version:
# Dependent variable, assignment condition,
# Optional: Covariates, sub-groups, cluster IDs, assignment review (Don't know what this is), balance variables

# Suggested To Dos in Kennedy version:
# - base() -> specify the base outcome when analyzing the assignments.
# - For multiple assignment options need to check balance across every possible assignment base.
# - Show table of covariate means across assignments.
# - Option or one-tailed or two-tailed p-values.
# - control() -> specify the assignment variable that is the control arm. presumed to be the lowest value if not specified.
# - auto(n) -> add automatic detection of continuous covariates if a variable exceeds a set number of levels, e.g. 32, or cardinality within the analyzed subset (e.g. > 5% of values are unique).

class fieldExAnalysis(object):
    """args:
    universeDf - a Pandas Data Frame object in which we'll run our analysis
    dv - The dependent variable, generally a survey response or vote history, which should have been recoded as a dummy variable by the user prior to calling this function. This must be a string, which must be the name of a column in data frame universeDf.
    condition - The treatment assignment condition. # TODO - Write code to automatically recode condition to 0/1 dummies
    control
    numOutputs - (optional) The number of outputs the user expects to exist in the dependent variable values. This is meant to be a useful check for the user to ensure what the expect matches the data the program is running on.
    covariates
    """
    def __init__(self, universeDf, dv, condition, control=None, numConditions = None, numOutputs=None, covariates=None): #TODO: Should treatment groups be acceptable as categorical variables, and we recode to 0/1s? I think yes. ID which var is control.
        self.universeDf = universeDf
        if not isinstance(self.universeDf, pd.DataFrame):
            raise Exception('Argument universeDf requires DataFrame object.')
        
        self.dv = dv
        if type(self.dv) != str:
            raise Exception('Argument \'dv\' must be a string.')
        # Check that the DV is a column in data frame universeDf
        elif self.dv not in self.universeDf.columns:
            raise Exception('Column {} does not exist in your data frame.'.format(self.dv))
        
        self.condition = condition
        if type(self.condition) != str:
            raise Exception('Argument \'condition\' must be a string.')
        # Check that the condition is a column in data frame universeDf
        elif self.condition not in self.universeDf.columns:
            raise Exception('Column {} does not exist in your data frame.'.format(self.condition))
            
        self.numOutputs = numOutputs # TODO: Use this one as a check with "proceed? y/n" option
        numOutputsObserved = len(set(self.universeDf[self.dv]))
        if self.numOutputs == None:
            self.numOutputs = numOutputsObserved
        if numOutputsObserved != self.numOutputs:
            raise Exception('Number of dependent variable outputs observed ({}) does not equal number of dependent variable outputs expected ({}). The number of dependent variable outputs should equal the number of treatment groups + 1 (for the control group).'.format(numOutputsObserved,self.numOutputs))
        
        self.numConditions = numConditions # TODO: Use this one as a check with "proceed? y/n" option
        numConditionsObserved = len(set(self.universeDf[self.condition]))
        if self.numConditions == None:
            self.numConditions = numConditionsObserved
        if numConditionsObserved != self.numConditions:
            raise Exception('Number of conditions observed ({}) does not equal number of conditions expected ({})..'.format(numConditionsObserved,self.numConditions))
        
        
        self.covariates = covariates
        if self.covariates != None:
            if not isinstance(self.covariates,list):
                raise Exception('Object "covariates" must be submitted as a list of strings. Default option is None. Use default if no covariate are to be used in analysis.')
        
        self.control = control
        if self.control == None:
            if 'control' in set(self.universeDf[self.condition]):
                self.control = 'control'
            elif 0 in set(self.universeDf[self.condition]):
                self.control = 0
            else:
                raise Exception('No control condition defined.')
        if self.control not in set(self.universeDf[self.condition]):
            raise Exception('Control condition "{}" does not appear in your data set.'.format(self.control))

            
    # Use this function if you want to evaluate the impact of multiple treatment assignments
    def reformatConditions(self):
        treatVars = list(set(self.universeDf[self.condition]))
        treatVars.remove(self.control)
                
        n = 1
        for var in treatVars:
            print ("Treatvar: {0}, n: {1}, treatvars list: {2}".format(var, n, treatVars))
            self.universeDf['treat_{}'.format(n)] = None
            # WRITE CODE HERE TO  REPLACE VALS
            
            n +=1
            

    
    #def analyzeLogit(self):


# TODO:
# Add code to deal with treatment conditions, ID control
# If more than one condition, logit each treatment group separately compared to control
# Write function to check for significant differences between treatment groups
# Code to create visuals: bar charts, tables; or nicely spit out numbers that can be quickly be dropped in a Microsoft PPT/Excel
