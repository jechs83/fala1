url = "//ripleype.imgix.net/https%3A%2F%2Fdpq25p1ucac70.cloudfront.net%2Fseller-place-files%2Fmrkl-files%2F589%2FMARKETPLACE%20INTERNACIONAL%2F416Qmb9xwYL_221714338603_61.jpeg?w=750&h=555&ch=Width&auto=format&cs=strip&bg=FFFFFF&q=60&trimcolor=FFFFFF&trim=color&fit=fillmax&ixlib=js-1.1.0&s=57f84713e79c42510d2323f069b44873"

url_start = url[:6]


if url_start != "https:":
    url = "https:"+url


print(url)

