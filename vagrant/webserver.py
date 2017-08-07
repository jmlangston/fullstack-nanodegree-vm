"""
Objectives
1. Modify server so that visiting localhost:8080/restaurants lists all of the 
restaurant names in the database. --> Add new if block to do_GET (/restaurants)
2. Add links to edit and delete each restaurant entry. Links don't need to do 
anything yet. --> Add markup for links to the for loop that adds restaurant names
3. Add capability to create a new restaurant: make a link on restaurants page that 
goes to another page where user can enter new restaurant name; new restaurant will
appear in the restaurant list. --> Add new if block to do_GET (/restaurants/new)
and new block to do_POST that handles adding new entry to database
4. Add capability to edit the name of a specific restaurant. Use URL restaurants/<id>/edit
--> Set href for 'Edit' anchor tag; show new page with form for editing name; update
name in database with POST request; redirect to main /restaurants/ page
5. Add capability to delete a restaurant. --> Set href for 'Delete' anchor tag;
show confirmation page; delete entry from database; redirect to main /restaurants/
page.
"""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi # common gateway interface

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# connect to the database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

# create a session to interface with the database
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200) # response code for successful GET
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()

                # html output
                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Make a new restaurant here</a><br><br>"
                for restaurant in restaurants:
                    output += restaurant.name + "<br>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a><br>" % restaurant.id
                    output += "<a href='/restaurants/%s/delete'>Delete</a><br><br>" % restaurant.id
                output += "</html></body>"

                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Make a new restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='newRestaurantName' type='text' placeholder='New restaurant name'>"
                output += "<input type='submit' value='Create'></form>"
                output += "</html></body>"

                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):

                restaurant_id = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "<html><body>"
                output += "<h1>%s</h1>" % restaurant.name
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurant.id
                output += "<input name='updatedName' type='text' placeholder='%s'>" % restaurant.name
                output += "<input type='submit' value='Rename'></form>"
                output += "</html></body>"

                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/delete"):
                restaurant_id = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "<html><body>"
                output += "<h1>Are you sure you want to delete %s?</h1>" % restaurant.name
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurant.id
                output += "<input type='submit' value='Delete'></form>"
                output += "</html></body>"

                self.wfile.write(output)
                print output
                return


            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Hello!"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "&#161Hola!"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')
                
                new_restaurant = Restaurant(name=messagecontent[0])
                session.add(new_restaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants') # redirect
                self.end_headers()
                return


            if self.path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('updatedName')

                restaurant_id = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

                restaurant.name = messagecontent[0]
                session.add(restaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants') # redirect
                self.end_headers()
                return


            if self.path.endswith('/delete'):
                restaurant_id = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                session.delete(restaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return

            if self.path.endswith('/hello'):
                self.send_response(301)
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

                output = ""
                output += "<html><body>"
                output += "<h2>Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
                output += "</body></html>"
            
                self.wfile.write(output)
                return

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()
