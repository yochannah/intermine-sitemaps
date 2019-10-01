#!/usr/bin/env python
#     http://intermine.readthedocs.org/en/latest/web-services/


from intermine.webservice import Service
import sys

intermine = sys.argv[1]

service = Service("http://www.flymine.org/flymine/service")

# Get a new query on the class (table) you will be querying:
query = service.new_query("Gene")

# The view specifies the output columns
query.add_view("primaryIdentifier")

# Uncomment and edit the line below (the default) to select a custom sort order:
#query.add_sort_order("Pathway.primaryIdentifier", "ASC")

# You can edit the constraint values below
query.add_constraint("primaryIdentifier", "IS NOT NULL", code = "A")

# You can edit the constraint values below
query.add_constraint("organism.name", "=", "Drosophila melanogaster", code = "B")

# Uncomment and edit the code below to specify your own custom logic:
# query.set_logic("A")

sitemapCount = 0;

prefix = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
prefix = prefix + "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n"
prefix = prefix + "  xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n"
prefix = prefix + "  xsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n"

postfix = "</urlset>"

rowCount = 0

f = open('sitemap' + str(sitemapCount) + ".xml",'wb')

f.write(prefix.encode('utf-8'))

for row in query.rows():
    content  = str("<url><loc>http://www.flymine.org/flymine/portal.do?externalids="
    + row["primaryIdentifier"].encode('utf-8').strip() + "</loc></url>\n")
    f.write(content.decode('utf_8'))
    rowCount = rowCount + 1
    if rowCount >= 50000:
        f.write(postfix)
        f.close()
        sitemapCount = sitemapCount + 1
        f = open('sitemap' + str(sitemapCount) + ".xml",'w')
        f.write(prefix)
        rowCount = 1
f.write(postfix)
f.close()
