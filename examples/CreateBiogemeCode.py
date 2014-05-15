#!/usr/local/bin/python

class BiogemeCode:
    '''
    Class to quickly create Biogeme code
    The result is not guaranteed to run perfectly, but should be 95% good
    '''
    
    def __init__(self, alternatives):
        self.alternatives = alternatives
        self.utility_function = []
        self.utility_prefix = []
        self.proxy = None
        self.coefficients = {}
        self.initial = {'start': 0, 'lower_bound': -100, \
                        'upper_bound': 100, 'estimate': 0}
        self.available_prefix = 'available_'
        self.choice_variable = 'chosen'
        self.weight_variable = None
        self.latent_class_function = None
        self.latent_class_prefix = None
        self.latent_class_proxy = None
        self.nests = []
        self.comments = ''

    def add_coefficients(self, coefficients, initial={}):
        '''
        Adds coefficients not included in utility function or latent class
        '''
        for b in coefficients:
            self.coefficients[b] = dict(self.initial, **initial)

    def _xb_to_coefficients(self, xb, operators=list('+-*/()')):
        '''
        Converts right hand side of an equation into coefficients
        Strips out operators and adds anything in all CAPS to coefficients
        '''
        for o in operators:
            xb = xb.replace(o, ' ')
        xb = xb.split()
        for b in xb:
            if b == b.upper():
                self.coefficients[b] = self.initial.copy()

    def add_utility(self, utility_function, proxy='#'):
        '''
        Sets utility information
        Anything on the right hand side in all CAPS becomes a coefficient
        '''
        self.utility_function.append(utility_function)
        v, xb = utility_function.split('=')
        self.utility_prefix.append(v.strip().replace(proxy, ''))
        self.proxy = proxy
        self._xb_to_coefficients(xb)

    def add_latent_class(self, latent_class_function, proxy='#'):
        '''
        Sets latent class information (based on existing utility_functions)
        Anything on the right hand side in all CAPS becomes a coefficient
        '''
        self.latent_class_function = latent_class_function
        c, xb = latent_class_function.split('=')
        self.latent_class_prefix = c.strip()
        self.latent_class_proxy = proxy
        for p in self.utility_prefix[0:-1]:
            xb_class = xb.replace(proxy, p)
            self._xb_to_coefficients(xb_class)

    def add_nest(self, nest):
        '''
        Sets nest information
        '''
        self.nests.append(nest)
        n = len(self.nests) - 1
        if n > 0:
            self.coefficients['SCALE' + str(n)] = self.initial.copy()

    def add_comment(self, comment):
        '''
        Adds comments to top of file
        '''
        self.comments = self.comments + '# ' + comment + '\n'

    def write_file(self, biogeme_file, fast=True):
        '''
        Writes code to file
        '''
        
        # Write header information
        fo = open(biogeme_file, mode='w')
        fo.write('# Biogeme model file ' + biogeme_file + '\n')
        fo.write(self.comments)
        fo.write('from biogeme import *\n')
        fo.write('from headers import *\n')
        fo.write('from nested import *\n')
        fo.write('from cnl import *\n')
        fo.write('from distributions import *\n')
        fo.write('from loglikelihood import *\n')
        fo.write('from statistics import *\n')
        
        # Write coefficients
        fo.write('\n# Specify coefficients\n')
        for b, initial in sorted(self.coefficients.items()):
            i = "', " + str(initial['start']) + ', ' + \
                str(initial['lower_bound']) + ', ' + \
                str(initial['upper_bound']) + ', ' + \
                str(initial['estimate']) + ')\n'
            if self.proxy in b:
                for alternative in self.alternatives:
                    a = str(alternative)
                    coefficient = b.replace(self.proxy, a)
                    fo.write(coefficient + " = Beta('" + coefficient + i)
            else:
                fo.write(b + " = Beta('" + b + i)
        
        # Write utilities
        fo.write('\n# Specify utility functions\n')
        for v in self.utility_function:
            for alternative in self.alternatives:
                a = str(alternative)
                fo.write(v.replace(self.proxy, a) + '\n')
            fo.write('\n')

        # Write utility lookup
        fo.write('# Specify utility lookup\n')
        for p in self.utility_prefix:
            fo.write(p + ' = {' + str(self.alternatives[0]) + ': ' + p + \
                     str(self.alternatives[0]) + ',\n')
            n = len(self.alternatives) - 1
            for i in range(1, n):
                a = str(self.alternatives[i])
                fo.write('     ' + a + ': ' + p + a + ',\n')
            fo.write('     ' + str(self.alternatives[n]) + ': ' + p + \
                     str(self.alternatives[n]) + '}\n')
            fo.write('\n')

        # Write availability lookup
        fo.write('# Specify availability lookup\n')
        fo.write('AV = {' + str(self.alternatives[0]) + ': ' + \
                 self.available_prefix + str(self.alternatives[0]) + ',\n')
        n = len(self.alternatives) - 1
        for i in range(1, n):
            a = str(self.alternatives[i])
            fo.write('      ' + a + ': ' + self.available_prefix + a + ',\n')
        fo.write('      ' + str(self.alternatives[n]) + ': ' + \
                 self.available_prefix + str(self.alternatives[n]) + '}\n')

        # Write latent class
        if self.latent_class_function:
            fo.write('\n# Latent class model\n')
            latent_class = []
            for p in self.utility_prefix[0:-1]:
                c = self.latent_class_function
                fo.write(c.replace(self.latent_class_proxy, p) + '\n')
                lcp = self.latent_class_prefix
                latent_class.append(lcp.replace(self.latent_class_proxy, p))
            for c1 in latent_class:
                fo.write('PROB_' + c1 + ' = exp(' + c1 + ') / (1')
                for c2 in latent_class:
                    fo.write(' + exp(' + c2 + ')')
                fo.write(')\n')
            lcp = self.latent_class_prefix
            lcp = lcp.replace(self.latent_class_proxy, self.utility_prefix[-1])
            fo.write('PROB_' + lcp + ' = 1')
            for c in latent_class:
                fo.write(' - PROB_' + c)
            fo.write('\n')

        # Write nested logit
        if len(self.nests) > 1:
            fo.write('\n# Define nests\n')
            fo.write('NEST0 = 1.0, ' + str(self.nests[0]) + '\n')
            nests = 'NESTS = NEST0'
            for n in range(1, len(self.nests)):
                nests = nests + ', NEST' + str(n)
                fo.write('NEST' + str(n) + ' = SCALE' + str(n) + ', ' + \
                         str(self.nests[n]) + '\n')
            fo.write(nests + '\n')

        # Write estimation information
        fo.write('\n# Maximize likelihood\n')
        fo.write("rowIterator('obsIter')\n")
        if len(self.nests) > 1:
            for p in self.utility_prefix:
                fo.write('PROB_' + p + ' = nested(' + p + ', AV, NESTS, ' + \
                         self.choice_variable + ')\n')
        else:
            for p in self.utility_prefix:
                fo.write('PROB_' + p + ' = bioLogit(' + p + ', AV, ' + \
                         self.choice_variable + ')\n')
        if self.weight_variable:
            fo.write('BIOGEME_OBJECT.WEIGHT = ' + self.weight_variable + '\n')
        if self.latent_class_function:
            lcp = self.latent_class_prefix
            p = self.utility_prefix[0]
            lcp = lcp.replace(self.latent_class_proxy, p)
            fo.write('PROB = PROB_' + lcp + ' * PROB_' + p)
            for p in self.utility_prefix[1:]:
                lcp = self.latent_class_prefix
                lcp = lcp.replace(self.latent_class_proxy, p)
                fo.write(' + PROB_' + lcp + ' * PROB_' + p)
            fo.write("\nBIOGEME_OBJECT.ESTIMATE = Sum(log(PROB), 'obsIter')\n")
        else:
            fo.write("BIOGEME_OBJECT.ESTIMATE = Sum(log(PROB_" + \
                     self.utility_prefix[0] + "), 'obsIter')\n")

        # Write parameter specifications
        fo.write('\n# Set optimization parameters\n')
        fo.write("BIOGEME_OBJECT.PARAMETERS['stopFileName'] = '" + biogeme_file + ".stop'\n")
        fo.write("BIOGEME_OBJECT.PARAMETERS['optimizationAlgorithm'] = 'BIO'\n")
        if fast:
            fo.write("BIOGEME_OBJECT.PARAMETERS['shareOfProcessors'] = '99'\n")
            fo.write("BIOGEME_OBJECT.PARAMETERS['BTRExactHessian'] = '0'\n")
            fo.write("BIOGEME_OBJECT.PARAMETERS['BTRCheapHessian'] = '1'\n")
            fo.write("BIOGEME_OBJECT.PARAMETERS['BTRInitQuasiNewtonWithTrueHessian'] = '0'\n")
            fo.write("BIOGEME_OBJECT.PARAMETERS['BTRInitQuasiNewtonWithBHHH'] = '1'\n")
            fo.write("BIOGEME_OBJECT.PARAMETERS['BTRUsePreconditioner'] = '1'\n")
            fo.write("BIOGEME_OBJECT.PARAMETERS['BTRQuasiNewtonUpdate'] = '1'\n")
            fo.write("BIOGEME_OBJECT.PARAMETERS['varCovarFromBHHH'] = '1'\n")
            fo.write("BIOGEME_OBJECT.PARAMETERS['deriveAnalyticalHessian'] = '0'\n")
            fo.write("BIOGEME_OBJECT.PARAMETERS['useAnalyticalHessianForOptimization'] = '0'\n")
            fo.write("BIOGEME_OBJECT.PARAMETERS['computeInitLoglikelihood'] = '0'")

        fo.close()
