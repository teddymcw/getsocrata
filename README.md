

When used as main() the returned json pages are saved in append mode as they are retrieved.  They are saved as lines of json serializable objects.  To load the resulting file, do so line-by-line with json.loads().

Current goal:

Track failed requests. Retry failed requests at the end. Timeout after a certain number of failed requests. This has the implicit assumption that the lines of json serialized objects are not ordered.

Record more metadata from requests. Is any metadata available from Socrata?

More logging.


