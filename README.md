A simple project for mailing list conversion from Sympa to L-Soft ListServ,
should you find yourself in similar circumstances.

The Sympa list config is parsed with 'sympa2json' to generate a Python dict which
can be manipulated by an number of output parsers.

The Lsoft config generator 'sjson2lsoft' converts the Sympa-json to a
list header for putting on the server.  It takes the list name and password as
the first to arguments

Run it in a pipeline like this
'''
sympa2json.py <sympa-config>  | ./sjson2lsoft.py <listname> <ownerpass>
'''

Get a list header by copying the listserv-config.json-ex file to 
listserv-config.json and changing the values for local configuration. Submit
the header (config) request with
'''
get-listconfig.py <listname>
'''
