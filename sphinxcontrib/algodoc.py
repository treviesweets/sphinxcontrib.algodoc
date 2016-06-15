# -*- coding: utf-8 -*-

### sphinxcontrib.algodoc ###
### sphinx function for step by step documentation of algorithms ###

import sys
import inspect
from docutils import nodes
from docutils.parsers.rst import directives, Directive, Parser


#class algodoc_node(nodes.Structural, nodes.Element):
#    pass

class AlgoDocDirective(Directive):

    # directive expected parmeters
    required_arguments = 1
    optional_arguments = 0
    
    # option spec
    option_spec = {'title':directives.unchanged,
                   'comment':directives.unchanged
                  }
    
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
                self.function = m[1]
             
        # load the source code for that module
        sourcelines = inspect.getsourcelines(self.function)[0]
       
        # POSSIBLY SHOULD BE USING NODES HERE
        
        
        idb = nodes.make_id(fct)
        node = nodes.section(ids=[idb])
        node += nodes.title(text = options['title'])
        node += nodes.paragraph(text = 'Function: ' + fct)
        
        if 'comment' in options.keys(): 
            node += nodes.paragraph(text = options['comment'])
                
        l1 = True
        
        # iterate through the source and find the comments
        for s in sourcelines:
            # all lines with comments are indicated with a '#:'
            if '#:' in s:                
                
                # comments should end with this
                if '#:#' in s:
                    l1 = True
                    
                else:
                    text = s.split('#:')[-1]

                    if l1:
                        node += nodes.strong(text = text)
                        l1 = False
                    else:
                        if len(text) > 1:
			    node += nodes.paragraph(text = '  *  ' + text)
                        else:
                            node += nodes.paragraph(text = text)        

        return [ node ]


def setup(app):
    #app.add_node(algodoc_node)
    app.add_directive('algodoc', AlgoDocDirective)
    #app.connect('autodoc-process-docstring', algodoc_proc_function)
    
    
if __name__ == '__main__':
    node = AlgoDocDirective()
    
