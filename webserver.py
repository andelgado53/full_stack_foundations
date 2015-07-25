from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy


engine = create_engine('sqlite:///shelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/shelters"):
                list_of_shelters = session.query(Shelter).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Shelters in the Area</h1>"
                for shelter in list_of_shelters:
                    output += '<h2><br>{0}</br></h2>'.format(shelter.name)
                    output += '<h3><a href="/shelters/{0}/edit">Edit</a></h3>'.format(shelter.id)
                    output += '<h3><a href="/shelters/{0}/delete">Delete</a></h3>'.format(shelter.id)
                output += '<h4><a href=/shelters/create>Create a new shelter</a></h4>'
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/shelters/create"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>New shelter creation form</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/shelters/create'>
                             <h2>Shelter Name:</h2>
                             <input name="sheltername" type="text" >
                             <br>
                             <h2>Address:</h2>
                             <input name="address" type="text" >
                             <br>
                             <h2>City:</h2>
                             <input name="city" type="text" >

                             <br>
                             <h2>State:</h2>
                             <input name="state" type="text" >

                             <br>
                             <h2>Zipcode:</h2>
                             <input name="zipcode" type="text" >

                             <br>
                             <h2>Website:</h2>
                             <input name="website" type="text" >
                             <br>
                             <input type="submit" value="Submit">
                             </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/edit'):
                shelter_id = int(self.path.split('/')[2])
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Edit the Name of a Shelter</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/shelters/{0}/edit'>
                             <h2>Shelter Name:</h2>
                             <input name="newsheltername" type="text" >
                             <input type="submit" value="Submit">
                             <br>
                             </form>'''
                output += "</body></html>"
                self.wfile.write(output.format(shelter_id))

            if self.path.endswith('/delete'):
                shelter_id = int(self.path.split('/')[2])
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                shelter_name = session.query(Shelter).filter_by(id=shelter_id).one().name
                output = ""
                output += "<html><body>"
                output += "<h1>Are you sure you want to delete shelter {0}?</h1>".format(shelter_name)
                output += '''<form method='POST' enctype='multipart/form-data' action='/shelters/{0}/delete'>

                             <input type="submit" value="Delete">
                             <br>
                             </form>'''.format(shelter_id)
                output += "</body></html>"
                self.wfile.write(output)



        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/shelters/create'):

                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    shelter_name = fields.get('sheltername')[0]
                    address = fields.get('address')[0]
                    city = fields.get('city')[0]
                    state = fields.get('state')[0]
                    zipcode = fields.get('zipcode')[0]
                    website = fields.get('website')[0]
                    if shelter_name:
                        new_shelter = Shelter(name=shelter_name, address=address,
                            city=city, state=state, zipCode=zipcode, website=website)
                        session.add(new_shelter)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        output = ""
                        output += "<html><body>"
                        output += " <h2> A new Shelter named has been entered to the database: </h2>"
                        output += "<h1>{0}</h1>".format(shelter_name)
                        output += "<h1>{0}</h1>".format(address)
                        output += '<a href=/shelters>Home</a>'
                        output += "</body></html>"
                        self.wfile.write(output)

            if self.path.endswith('/edit'):
                #print(self.path.split('/'))
                shelter_id = int(self.path.split('/')[2])
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_shelter_name = fields.get('newsheltername')[0]
                    shelter = session.query(Shelter).filter_by(id=shelter_id)
                    for se in shelter:
                        se.name = new_shelter_name
                    session.commit()
                    self.send_response(301)
                    self.send_header('Location', '/shelters')
                    self.end_headers()
            if self.path.endswith('/delete'):
                shelter_id = int(self.path.split('/')[2])
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    shelter_to_delete = session.query(Shelter).filter_by(id=shelter_id).one()
                    session.delete(shelter_to_delete)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Location', '/shelters')
                    self.end_headers()
                    sefl.wfile.write('hello world')




        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()