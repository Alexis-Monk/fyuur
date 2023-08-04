#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, make_response
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from datetime import datetime


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String)
    image_link = db.Column(db.String)
    facebook_link = db.Column(db.String)
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venue', lazy=True)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artist', lazy=True)


class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  venue_name = db.Column(db.String(120), nullable=False)
  venue_image_link = db.Column(db.String(500))
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  artist_name = db.Column(db.String(120), nullable=False)
  artist_image_link = db.Column(db.String(500))
  start_time = db.Column(db.DateTime, nullable=False)

# if the tables exist but are empty, seed them
conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])
cursor = conn.cursor()
cursor.execute('select count(*) as count from pg_tables where tablename in (\'Venue\', \'Show\', \'Artist\')')
row = cursor.fetchone()
if row[0] == 3:
  cursor.execute('select count(a.id) as count from (select id from "Artist" b union select id from "Show" c union select id from "Venue" d) a')
  row = cursor.fetchone()
  if row[0] == 0:

    venue1 = Venue(
      name='The Musical Hop',
      genres=['Jazz','Reggae','Swing','Classical','Folk'],
      address='1015 Folsom Street',
      city='San Francisco',
      state='CA',
      phone='123-123-1234',
      website='https://www.themusicalhop.com',
      facebook_link='https://www.facebook.com/TheMusicalHop',
      seeking_talent=True,
      seeking_description='We are on the lookout for a local artist to play every two weeks. Please call us.',
      image_link='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60'
    )
    venue2 = Venue(
      name='The Dueling Pianos Bar',
      genres=['Classical','R&B','Hip-Hop'],
      address='336 Delancey Street',
      city='New York',
      state='NY',
      phone='914-003-1132',
      website='https://www.theduelingpianos.com',
      facebook_link='https://www.facebook.com/theduelingpianos',
      seeking_talent=False,
      image_link='https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80'
    )
    venue3 = Venue(
      name='Park Square Live Music & Coffee',
      genres=['Rock n Roll','Jazz','Classical','Folk'],
      address='34 Whiskey Moore Ave',
      city='San Francisco',
      state='CA',
      phone='415-000-1234',
      website='https://www.parksquarelivemusicandcoffee.com',
      facebook_link='https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
      seeking_talent=False,
      image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80'
    )
    artist1 = Artist(
      name='Guns n Petals',
      genres=['Rock n Roll'],
      city='San Francisco',
      state='CA',
      phone='326-123-5000',
      website='https://www.gunsnpetalsband.com',
      facebook_link='https://www.facebook.com/GunsNPetals',
      seeking_venue=True,
      seeking_description='Looking for shows to perform at in the San Francisco Bay Area!',
      image_link='https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'
    )
    artist2 = Artist(
      name='Matt Quevedo',
      genres=['Jazz'],
      city='New York',
      state='NY',
      phone='300-400-5000',
      facebook_link='https://www.facebook.com/mattquevedo923251523',
      seeking_venue=False,
      image_link='https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80'
    )
    artist3 = Artist(
      name='The Wild Sax Band',
      genres=['Jazz','Classical'],
      city='San Francisco',
      state='CA',
      phone='432-325-5432',
      seeking_venue=False,
      image_link='https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80'
    )
    show1 = Show(
      venue_id=1,
      venue_name='The Musical Hop',
      venue_image_link='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
      artist_id=1,
      artist_name='Guns N Petals',
      artist_image_link='https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
      start_time='2019-05-21T21:30:00.000Z'
    )
    show2 = Show(
      venue_id=3,
      venue_name='Park Square Live Music & Coffee',
      venue_image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
      artist_id=2,
      artist_name='Matt Quevedo',
      artist_image_link='https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',
      start_time='2019-06-15T23:00:00.000Z'
    )
    show3 = Show(
      venue_id=3,
      venue_name='Park Square Live Music & Coffee',
      venue_image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
      artist_id=3,
      artist_name='The Wild Sax Band',
      artist_image_link='https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
      start_time='2035-04-01T20:00:00.000Z'
    )
    show4 = Show(
      venue_id=3,
      venue_name='Park Square Live Music & Coffee',
      venue_image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
      artist_id=3,
      artist_name='The Wild Sax Band',
      artist_image_link='https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
      start_time='2035-04-08T20:00:00.000Z'
    )
    show5 = Show(
      venue_id=3,
      venue_name='Park Square Live Music & Coffee',
      venue_image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
      artist_id=3,
      artist_name='The Wild Sax Band',
      artist_image_link='https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
      start_time='2035-04-15T20:00:00.000Z'
    )
    db.session.add(venue1)
    db.session.add(venue2)
    db.session.add(venue3)
    db.session.add(artist1)
    db.session.add(artist2)
    db.session.add(artist3)
    db.session.add(show1)
    db.session.add(show2)
    db.session.add(show3)
    db.session.add(show4)
    db.session.add(show5)
    db.session.commit()


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = datetime.now()
  if type(value) is not datetime:
    date = dateutil.parser.parse(value)
  else:
    date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

from sqlalchemy import func

@app.route('/venues')
def venues():
    venues_data = Venue.query.all()

    data = {}
    for venue in venues_data:
        area_key = f'{venue.city}{venue.state}'
        if area_key not in data:
            data[area_key] = {
                'city': venue.city,
                'state': venue.state,
                'venues': []
            }

        num_upcoming_shows = db.session.query(func.count(Show.id)).filter(Show.venue_id == venue.id, Show.start_time > datetime.now()).scalar()

        venue_info = {
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': num_upcoming_shows
        }

        data[area_key]['venues'].append(venue_info)

    return render_template('pages/venues.html', areas=data.values())


from sqlalchemy import or_

@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form['search_term']
    search_pattern = f'%{search_term}%'

    venues = Venue.query.filter(or_(Venue.name.ilike(search_pattern), Venue.city.ilike(search_pattern), Venue.state.ilike(search_pattern)))

    venue_data = []
    for venue in venues:
        num_upcoming_shows = db.session.query(func.count(Show.id)).filter(Show.venue_id == venue.id, Show.start_time > datetime.now()).scalar()
        venue_info = {
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': num_upcoming_shows
        }
        venue_data.append(venue_info)

    response = {
        "count": len(venue_data),
        "data": venue_data
    }

    return render_template('pages/search_venues.html', results=response, search_term=search_term)

from sqlalchemy import and_

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)

    upcoming_shows = db.session.query(Show).filter(and_(Show.venue_id == venue_id, Show.start_time > datetime.now())).all()
    past_shows = db.session.query(Show).filter(and_(Show.venue_id == venue_id, Show.start_time < datetime.now())).all()

    venue.upcoming_shows = [{
        'artist_id': show.artist_id,
        'artist_name': show.artist.name,
        'artist_image_link': show.artist.image_link,
        'start_time': show.start_time.strftime('%Y-%m-%dT%H:%M:%S')
    } for show in upcoming_shows]

    venue.past_shows = [{
        'artist_id': show.artist_id,
        'artist_name': show.artist.name,
        'artist_image_link': show.artist.image_link,
        'start_time': show.start_time.strftime('%Y-%m-%dT%H:%M:%S')
    } for show in past_shows]

    venue.upcoming_shows_count = len(upcoming_shows)
    venue.past_shows_count = len(past_shows)

    return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        genres = request.form.getlist('genres')
        seeking_talent = True if request.form.get('seeking_talent') == 'y' else False

        venue = Venue(
            name=request.form['name'],
            genres=genres,
            city=request.form['city'],
            state=request.form['state'],
            address=request.form['address'],
            phone=request.form['phone'],
            website=request.form['website_link'],
            image_link=request.form['image_link'],
            facebook_link=request.form['facebook_link'],
            seeking_talent=seeking_talent,
            seeking_description=request.form['seeking_description']
        )

        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed. Error: ' + str(e), 'error')
    finally:
        db.session.close()

    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        venue = Venue.query.get(venue_id)
        if venue is not None:
            db.session.delete(venue)
            db.session.commit()
            flash('Venue was successfully deleted!')
        else:
            flash('Venue with ID ' + venue_id + ' does not exist.', 'error')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the venue. Error: ' + str(e), 'error')
    finally:
        db.session.close()

    return make_response('Success', 200)


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.order_by(Artist.name).all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form['search_term']
    search_pattern = f'%{search_term}%'

    artists = Artist.query.filter(Artist.name.ilike(search_pattern)).all()

    artist_data = []
    for artist in artists:
        num_upcoming_shows = db.session.query(func.count(Show.id)).filter(Show.artist_id == artist.id, Show.start_time > datetime.now()).scalar()
        artist_info = {
            'id': artist.id,
            'name': artist.name,
            'num_upcoming_shows': num_upcoming_shows
        }
        artist_data.append(artist_info)

    response = {
        "count": len(artist_data),
        "data": artist_data
    }

    return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)

    upcoming_shows = db.session.query(Show).filter(and_(Show.artist_id == artist_id, Show.start_time > datetime.now())).all()
    past_shows = db.session.query(Show).filter(and_(Show.artist_id == artist_id, Show.start_time < datetime.now())).all()

    artist.upcoming_shows = [{
        'venue_id': show.venue_id,
        'venue_name': show.venue.name,
        'venue_image_link': show.venue.image_link,
        'start_time': show.start_time.strftime('%Y-%m-%dT%H:%M:%S')
    } for show in upcoming_shows]

    artist.past_shows = [{
        'venue_id': show.venue_id,
        'venue_name': show.venue.name,
        'venue_image_link': show.venue.image_link,
        'start_time': show.start_time.strftime('%Y-%m-%dT%H:%M:%S')
    } for show in past_shows]

    artist.upcoming_shows_count = len(upcoming_shows)
    artist.past_shows_count = len(past_shows)

    return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  is_error = False
  requestGenres = request.form['genres']
  genres = [requestGenres] if type(requestGenres) == str else request.form.getlist('genres')
  try:
    artist = Artist.query.get(artist_id)
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = genres
    artist.facebook_link = request.form['facebook_link']
    artist.image_link = request.form['image_link']
    artist.website = request.form['website_link']
    artist.seeking_venue = request.form['seeking_venue'] == 'y' if 'seeking_venue' in request.form else False
    artist.seeking_description = request.form['seeking_description']
    db.session.commit()
  except:
    is_error = True
    db.session.rollback()
  finally:
    db.session.close()
  
  if not is_error:
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  else:
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.', 'error')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  is_error = False
  requestGenres = request.form['genres']
  genres = [requestGenres] if type(requestGenres) == str else request.form.getlist('genres')
  try:
    venue = Venue.query.get(venue_id)
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.genres = genres
    venue.facebook_link = request.form['facebook_link']
    venue.image_link = request.form['image_link']
    venue.website = request.form['website_link']
    venue.seeking_talent = request.form['seeking_talent'] == 'y'
    venue.seeking_description = request.form['seeking_description']
    db.session.commit()
  except:
    is_error = True
    db.session.rollback()
  finally:
    db.session.close()
  
  if not is_error:
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  else:
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.', 'error')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
        genres = request.form.getlist('genres')
        seeking_venue = True if request.form.get('seeking_venue') == 'y' else False

        artist = Artist(
            name=request.form['name'],
            genres=genres,
            city=request.form['city'],
            state=request.form['state'],
            phone=request.form['phone'],
            website=request.form['website_link'],
            image_link=request.form['image_link'],
            facebook_link=request.form['facebook_link'],
            seeking_venue=seeking_venue,
            seeking_description=request.form['seeking_description']
        )

        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed. Error: ' + str(e), 'error')
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

from datetime import datetime

@app.route('/shows')
def shows():
    shows_data = Show.query.order_by(Show.start_time.desc()).all()
    shows = []

    for show in shows_data:
        show_info = {
            'venue_id': show.venue.id,
            'venue_name': show.venue.name,
            'artist_id': show.artist.id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time.strftime('%Y-%m-%dT%H:%M:%S')
        }
        shows.append(show_info)

    return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create', methods=['GET'])
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        artist_id = request.form['artist_id']
        venue_id = request.form['venue_id']
        start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M:%S')

        artist = Artist.query.get(artist_id)
        venue = Venue.query.get(venue_id)

        show = Show(
            venue=venue,
            artist=artist,
            start_time=start_time
        )

        db.session.add(show)
        db.session.commit()
        flash(f'Show with artist id {artist_id} and venue id {venue_id} was successfully listed!')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred. Show with artist id {artist_id} and venue id {venue_id} could not be listed. Error: {str(e)}', 'error')
    finally:
        db.session.close()

    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

from logging import Formatter, FileHandler

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('Errors')

    # Remove the following block if you want to use the built-in Flask error handling for non-500 errors
    @app.errorhandler(Exception)
    def unhandled_exception(e):
        app.logger.error('Unhandled Exception: %s', (e))
        return render_template('errors/500.html'), 500

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
