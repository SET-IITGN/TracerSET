def http_status(status): 
    match status:
        case 400:
            return "Bad Request" 
        case 401:
            return "Unauthorized"
        case 403:
            return "Forbidden"
        case 404:
            return "Not Found"
        case 200:
            return "Ok" 
        case 201:
            return "Created" 
        case 500:
            return "Internal Server Error"
        case _:
            return "Unknown Status" 
n=int(input()) 
print(http_status(n))


