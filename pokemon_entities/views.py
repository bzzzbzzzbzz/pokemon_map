import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime

from .models import PokemonEntity, Pokemon



MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemon_image = get_pokemon_photo(request, pokemon)
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon_image,
            'title_ru': pokemon.title,
        })
    time_now = localtime().now()
    pokemons_entity = PokemonEntity.objects.filter(appeared_at__lt=time_now, disappeared_at__gt=time_now)
    for pokemon_entity in pokemons_entity:
        pokemon_image = get_pokemon_photo(request, pokemon_entity.pokemon)
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_image,
        )

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    chosen_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_image = get_pokemon_photo(request, chosen_pokemon)
    pokemon_detail = {
        "title_ru": chosen_pokemon.title,
        "title_en": chosen_pokemon.title_en,
        "title_jp": chosen_pokemon.title_jp,
        "description": chosen_pokemon.description,
        "img_url": pokemon_image,
    }
    time_now = localtime().now()
    pokemons_entity = chosen_pokemon.entities.filter(appeared_at__lt=time_now,
                                                     disappeared_at__gt=time_now)

    for pokemon_entity in pokemons_entity:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_image
        )

    pokemon = chosen_pokemon.next_evolutions.first()
    if pokemon:
        pokemon_photo = get_pokemon_photo(request, pokemon)
        pokemon_detail['next_evolution'] = {
            "title_ru": pokemon.title,
            "pokemon_id": pokemon.id,
            "img_url": pokemon_photo
        }

    pokemon = chosen_pokemon.previous_evolution
    if pokemon:
        pokemon_photo = get_pokemon_photo(request, pokemon)
        pokemon_detail['previous_evolution'] = {
            "title_ru": pokemon.title,
            "pokemon_id": pokemon.id,
            "img_url": pokemon_photo
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_detail
    })


def get_pokemon_photo(request, pokemon):
    return request.build_absolute_uri(pokemon.image.url) if pokemon.image else DEFAULT_IMAGE_URL