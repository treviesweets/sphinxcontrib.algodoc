# -*- coding: utf-8 -*-

### sphinxcontrib.algodoc ###
### sphinx function for step by step documentation of algorithms ###

import sys
import inspect
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive

#class algodoc_node(nodes.Structural, nodes.Element):
#    pass

class AlgoDocDirective(Directive):

    # directive expected parmeters
    required_arguments = 1
    optional_arguments = 0
    
    # example option spec
    option_spec = {'function':directives.unchanged}
    
    final_argument_whitespace = True
    has_content = True

    ## CAREFUL WITH OVERRIDING INIT YOU DUMMY ##
    
    def run(self):
                
        env = self.state.document.settings.env
        config = env.config
        
        arguments = self.arguments # this is the function to look for
        options = self.options

        # split out function, module, class names
        fct = arguments[0] # assume the function is the first (only) arg
        fct_split = fct.split('.')
        
        # if it's a function not a method len(fct_split) == 2
        if len(fct_split) == 2:
            self.module_name = fct_split[0]
            self.class_name = None
            self.function_name = fct_split[1]
        
        elif len(fct_split) == 3:
            self.module_name = fct_split[0]
            self.class_name = fct_split[1]
            self.function_name = fct_split[2]
        
        else:
            return None
           
        # this bit is inspired by autodoc...
        # import the module
        
        __import__(self.module_name)

        # get a reference to the module by name
        mod = sys.modules[self.module_name]
                        
        # if we're looking for a method then search for the class
        if self.class_name is not None:
            for m in inspect.getmembers(mod):
                if m[0] == self.class_name:
                    members = inspect.getmembers(m[1])
        else:
            # get all the stuff defined in that module
            members = inspect.getmembers(mod)

        # iterate through the resulting list and find the function
        for m in members:
            if m[0] == self.function_name:
                fct = m[1]
             
        # load the source code for that module
        sourcelines = inspect.getsourcelines(fct)[0]
       
        # POSSIBLY SHOULD BE USING NODES HERE
        
        comments = [] # recieves all the comments
        comment = [] # recieves individual comments

        # iterate through the source and find the comments
        for s in sourcelines:
            # all lines with comments are indicated with a '#:'
            if '#:' in s:
                print s
                print type(s)
                
                # comments should end with this
                if '#:#' in s:
                    comments.append(comment)
                    comment = []
                else:
                    comment.append(s.split('#:')[-1])
         
        print comments
        
        
        # the html document
        # print self.state.document
        # print inspect.getsourcelines(function)
        # print env.temp_data.get(function)
        
        # print app
        # print what
        # print obj
        
        node = nodes.paragraph()
        node += nodes.section()
        
        return [ node ]

def algodoc_proc_function(app, what, name, obj, options, lines):
    print 'autodoc hook'
    print app
    print what
    print obj
    

def setup(app):
    #app.add_node(algodoc_node)
    app.add_directive('algodoc', AlgoDocDirective)
    #app.connect('autodoc-process-docstring', algodoc_proc_function)
    
    
if __name__ == '__main__':
    node = AlgoDocDirective()
    