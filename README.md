# Basic_Web_Server

## Hello, I will show you how to run my basic web server. Before we begin, I'll explain some things my web server can do:  
    - Listen for incoming connections from a web browser or HTTP client  
    - Respond to GET requests with appropriate status codes (e.g. 200 OK, 404 Not Found)  
    - Serve basic files (.html, .json, .js. txt, .css, and more) from a directory  
    - Handle different types of content (see previous bullet point for file types) which can be tested via running the web server  
    - Log each request, displaying request method, URL, and status in a clear format in the command line  
    - Handle timeouts  

## Now, how to use and test my web server:  
  
    1. Make sure you have python or python3 installed (I personally have/used python3). You can check using "python --version" or "python3 --version"  
      
    2. Now, go to your web browser or any HTTP client. I prefer the web browser for this and recommend it
        
    3. To test our web server amongst the different requests, here are all the links you should enter on your web browser:  
    http://localhost:8080/  
    http://localhost:8080/examples.json  
    http://localhost:8080/index.html
    http://localhost:8080/404.html  
    http://localhost:8080/plain.txt  
    http://localhost:8080/red.css  
    http://localhost:8080/javascript.js  
    http://localhost:8080/qowir8uqidjasd  
    http://localhost:8080/jfksdkjfhaksjdhfkjasdhf  
    http://localhost:8080/thisisdefinetelynotapagethatexists  
        
    4. You should notice that the web server accurately serves the right file when it exists and WHEN IT DOESN'T, it defaults to the 404 Not Found page. And when we are at our /, we are always at index.html
        
    5. In a similar manner, visiting /index.html and /404.html will also serve those exact pages as our web server checks and sees they exist so they accurately serve it
        
    6. Lastly, to check our server can handle timeouts, open a separate terminal tab while having the server running in your other terminal tab  
        
    7. Make sure you have telnet installed. You can check using "telnet --version"  
             
    8. Connect to our server through the command "telnet localhost 8080"    
      
    9. Do not type anything and since our server is coded to time-out after 10 seconds, you'll notice this is exactly what happens    
      
    10. This is our web server!

