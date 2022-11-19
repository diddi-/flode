
# Nomenclature

**Endpoint**

An endpoint is responsible for receiving and handle a http request and return a response.
This is the actual user method that handles the request.

**Controller**

Controllers should *not* be used within this project.

**Route**

A Route connects a Path with an Endpoint. It is what allows the routing middleware to know where to send the request.
It is neither a Path nor an Endpoint, it's a combination of the two.

**Path**

A Path is the portion of the URL that specify where the user want to navigate on the server. For example, given the URL 
`http://my.server.com/user/1/profile` the *Path* is `/user/1/profile`
