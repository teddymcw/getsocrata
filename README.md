

When used as main() the returned json pages are saved in append mode as they are retrieved.  They are saved as lines of json serializable objects.  To load the resulting file, do so line-by-line with json.loads().

Current goal:

Track failed requests. Retry failed requests at the end. Timeout after a certain number of failed requests. This has the implicit assumption that the lines of json serialized objects are not ordered.

Record more metadata from requests. Is any metadata available from Socrata?

More logging.


Socrata's explanation of throttling:
=======
Throttling and Applications Tokens    
Hold on a second! Before you go storming off to make the next great open data app, you should understand how SODA handles throttling. You can make a certain certain number of requests without an application token, but they come from a shared pool and you.re eventually going to get cut off.    
If you want more requests, register for an application token and your application will be granted up to 1000 requests per rolling hour period. If you need even more than that, special exceptions are made by request. Use the Help! tab on the right of this page to file a trouble ticket.    
Filtering data via a SODA API is fairly straightforward. There are two primary mechanisms you can use to filter data: Simple Filters and SoQL Queries    
