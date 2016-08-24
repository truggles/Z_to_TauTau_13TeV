#!/usr/bin/env python
import json

def das_query ( query ) :
  '''
  returns json object with result of query
  '''
  import subprocess
  cmd = ['das_client',
      '--limit=0',
      '--format=json',
      '--query="%s"' % query]
  output = subprocess.Popen(" ".join(cmd), shell=True, stdout=subprocess.PIPE).stdout
  result = json.load(output)
  if result['status'] != 'ok' :
    rtn = 'DAS query returned result status %s' % result['status']
    raise Exception(rtn)
  return result

if __name__ == '__main__' :
  import sys
  result = das_query(sys.argv[1])
  print json.dumps(result, indent=4)
