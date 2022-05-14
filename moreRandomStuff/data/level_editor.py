#!/usr/bin/python3.4
# Setup Python ----------------------------------------------- #
import pygame, sys, random, json
import tile_map, spritesheet_loader, text
from core_funcs import *
from tkinter import filedialog
from tkinter import *
import pyperclip

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('level editor')
display_size = [600, 400]
display_scale = 2
particle_speed = 0.5
particle_duration = 1
particle_rate = 10
screen = pygame.display.set_mode((display_size[0] * display_scale, display_size[1] * display_scale),0,32)

display = pygame.Surface(display_size)

def auto_tile(selection_points, level_map, layer, selected_spritesheet):
    global auto_tile_config, spritesheets
    tile_list = get_selection_pos_list(selection_points)
    tile_index_list = [b['tile'] for b in auto_tile_config['tile_borders']]
    if len(spritesheets[selected_spritesheet]) >= max(tile_index_list) + 1:
        for tile in tile_list:
            tile_dat = level_map.get_tile(tile, target_layer=layer)
            if tile_dat:
                found_locs = []
                for loc in auto_tile_config['check_list']:
                    search_loc = [loc[0] + tile[0], loc[1] + tile[1]]
                    if level_map.get_tile(search_loc, target_layer=layer):
                        found_locs.append(loc)
                for tile_setting in auto_tile_config['tile_borders']:
                    if sorted(tile_setting['border_list']) == sorted(found_locs):
                        tile_row = tile_setting['tile']
                        tile_col = random.randint(0, len(spritesheets[selected_spritesheet][tile_row]) - 1)
                        tile_dat['type'] = [selected_spritesheet, tile_row, tile_col]
                        tile_dat['raw'][1] = tile_dat['type'].copy()

def floodfill(pos, level_map, tile_dat, layer):
    global square_effects
    remaining_tiles = [pos]
    while remaining_tiles != []:
        remaining_tiles_c = remaining_tiles.copy()
        remaining_tiles = []
        for tile in remaining_tiles_c:
            level_map.add_tile(tile_dat.copy(), tile, layer)
            square_effects.append({'pos': tile, 'size': (tile_size, tile_size)})
            bordering_tiles = [[tile[0] + 1, tile[1]],
                               [tile[0] - 1, tile[1]],
                               [tile[0], tile[1] + 1],
                               [tile[0], tile[1] - 1]]
            for b_tile in bordering_tiles:
                if not level_map.get_tile(b_tile, layer):
                    if b_tile not in remaining_tiles:
                        remaining_tiles.append(b_tile)

def get_selection_pos_list(selection_points):
    selection_points = rect_corners(selection_points)
    start = [int(round(selection_points[0][0] / tile_size - 0.5, 0)), int(round(selection_points[0][1] / tile_size - 0.5, 0))]
    end = [int(round(selection_points[1][0] / tile_size - 0.5, 0)), int(round(selection_points[1][1] / tile_size - 0.5, 0))]
    return points_between_2d([start, end])

spritesheets, spritesheets_data = spritesheet_loader.load_spritesheets('images/spritesheets/')
spritesheet_keys = list(spritesheets.keys())
spritesheet_keys.sort()
font = text.Font('fonts/small_font.png', (208, 223, 215))

auto_tile_config = json.loads(read_f('auto_tile_config.json'))

tile_size = 18

level_map = tile_map.TileMap((tile_size, tile_size), (600, 400))
scroll = [0, 0]

up = False
down = False
right = False
left = False
click = False
clicking = False
right_clicking = False
ctrl = False
shift = False

typing_mode = False

layer_opacity = False

scroll_speed = 5
side_bar_size = 130

current_selection = [None, None]
spritesheet_scroll = 0
spritesheet_img_scroll = 0
spritesheet_img_scroll_y = 0
selected_spritesheet = None
selected_tile = None
placement_mode = 'grid_tiles'
current_layer = 0
deleted_tiles = []
particles = []
square_effects = []

custom_text = ''
typing_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', ';', ',']

# Loop ------------------------------------------------------- #
while True:

    # Background --------------------------------------------- #
    hovering_spritesheet_list = False
    hovering_spritesheet_images = False
    display.fill((0,0,0))
    mx, my = pygame.mouse.get_pos()
    mx = int(mx / display_scale)
    my = int(my / display_scale)

    if right:
        scroll[0] += scroll_speed
    if left:
        scroll[0] -= scroll_speed
    if up:
        scroll[1] -= scroll_speed
    if down:
        scroll[1] += scroll_speed

    # Square Effects ----------------------------------------- #
    for i, square_effect in sorted(enumerate(square_effects), reverse=True):
        square_effect = square_effects[i]
        if 'width' not in square_effect:
            square_effect['width'] = 3
            square_effect['speed'] = 1.5
            if 'render_pos' in square_effect:
                square_effect['pos'] = [square_effect['pos'][0] * tile_size, square_effect['pos'][1] * tile_size]
            else:
                square_effect['pos'] = list(square_effect['pos'])
            square_effect['size'] = list(square_effect['size'])
        square_effect['speed'] -= 0.05
        square_effect['width'] -= 0.1
        speed = square_effect['speed']
        square_effect['pos'][0] -= speed / 2
        square_effect['pos'][1] -= speed / 2
        square_effect['size'][0] += speed
        square_effect['size'][1] += speed
        r = pygame.Rect(square_effect['pos'][0] - scroll[0], square_effect['pos'][1] - scroll[1], square_effect['size'][0], square_effect['size'][1])
        pygame.draw.rect(display, (255, 255, 255), r, math.ceil(square_effect['width']))
        if square_effect['width'] <= 0:
            square_effects.pop(i)

    # Render Tiles ------------------------------------------- #
    render_list = level_map.get_visible(scroll)
    for layer in render_list:
        layer_id = layer[0]
        for tile in layer[1]:
            offset = [0, 0]
            if tile[1][0] in spritesheets_data:
                tile_id = str(tile[1][1]) + ';' + str(tile[1][2])
                if tile_id in spritesheets_data[tile[1][0]]:
                    if 'tile_offset' in spritesheets_data[tile[1][0]][tile_id]:
                        offset = spritesheets_data[tile[1][0]][tile_id]['tile_offset']
            img = spritesheet_loader.get_img(spritesheets, tile[1])
            if layer_opacity:
                if layer_id != current_layer:
                    img = img.copy()
                    img.set_alpha(100)
            display.blit(img, (tile[0][0] - scroll[0] + offset[0], tile[0][1] - scroll[1] + offset[1]))

    # Particles ---------------------------------------------- #
    for tile in deleted_tiles:
        img = spritesheet_loader.get_img(spritesheets, tile['type'])
        img_colorkey = img.get_colorkey()
        center = [img.get_width() / 2, img.get_height() / 2]
        for y in range(img.get_height()):
            for x in range(img.get_width()):
                c = img.get_at((x, y))
                if img_colorkey:
                    if (c[0] == img_colorkey[0]) and (c[1] == img_colorkey[1]) and (c[2] == img_colorkey[2]):
                        continue
                # loc, vel, color, dur
                if random.randint(1, particle_rate) == 1:
                    center_angle = angle_to([center, (x, y)])
                    speed = random.randint(int(10 * particle_speed / 4), int(10 * particle_speed)) / 10
                    dur = random.randint(0, int(particle_duration * 100)) / 100
                    particles.append([[tile['raw'][0][0] + x, tile['raw'][0][1] + y], [math.cos(center_angle) * speed, math.sin(center_angle) * speed], c, dur])
    deleted_tiles = []

    for i, particle in sorted(enumerate(particles), reverse=True):
        particle = particles[i]
        display.set_at((int(particle[0][0] - scroll[0]), int(particle[0][1] - scroll[1])), particle[2])
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[1][1] += 0.03
        particle[3] -= 1 / 60
        if particle[3] < 0:
            particles.pop(i)

    # Selection ---------------------------------------------- #
    if current_selection != [None, None]:
        selection_points = [current_selection[0], current_selection[1]]
        if current_selection[1] == None:
            selection_points[1] = (mx + scroll[0], my + scroll[1])
        selection_r = corner_rect(selection_points)

        # render
        selection_r.x -= scroll[0]
        selection_r.y -= scroll[1]
        pygame.draw.rect(display, (255, 0, 255), selection_r, 1)

    # GUI ---------------------------------------------------- #
    base_hover_x = mx + scroll[0]
    base_hover_y = my + scroll[1]

    currently_hovering = level_map.get_by_rect(pygame.Rect(base_hover_x, base_hover_y, 2, 2))

    font.render('Hovering IDs', display, (display.get_width() - font.width('Hovering IDs') - 2, 12))
    id_text = ''
    base_y = 22
    for tile in currently_hovering:
        if len(tile) > 2:
            font.render(str(tile[2]), display, (display.get_width() - font.width(str(tile[2])) - 2, base_y))
            base_y += 10
            id_text += str(tile[2]) + '\n'
    if id_text != '':
        id_text = id_text[:-1]

    hover_x = int(round(base_hover_x / tile_size - 0.5, 0))
    hover_y = int(round(base_hover_y / tile_size - 0.5, 0))
    if right_clicking and (mx > side_bar_size):
        if placement_mode == 'grid_tiles':
            deleted_tile = level_map.remove_tile((hover_x, hover_y), layer=current_layer)
            if deleted_tile:
                deleted_tiles.append(deleted_tile)
        elif placement_mode == 'off_grid_tiles':
            deleted_tile_group = level_map.remove_off_grid_tiles(pygame.Rect(base_hover_x, base_hover_y, tile_size, tile_size), layer=current_layer)
            for deleted_tile in deleted_tile_group:
                deleted_tiles.append(deleted_tile)
    if selected_tile:
        img = spritesheet_loader.get_img(spritesheets, selected_tile).copy()
        img.set_alpha(150)
        if placement_mode == 'grid_tiles':
            display.blit(img, (hover_x * tile_size - scroll[0], hover_y * tile_size - scroll[1]))
            if clicking and (mx > side_bar_size):
                new_tile_dat = selected_tile.copy()
                level_map.add_tile(new_tile_dat, (hover_x, hover_y), current_layer)
                square_effects.append({'pos': (hover_x * tile_size, hover_y * tile_size), 'size': (tile_size, tile_size)})
        elif placement_mode == 'off_grid_tiles':
            display.blit(img, (mx, my))
            if click and (mx > side_bar_size):
                new_tile_dat = selected_tile.copy()
                level_map.add_off_grid_tile(new_tile_dat, (base_hover_x, base_hover_y), current_layer)
                square_effects.append({'pos': (base_hover_x, base_hover_y), 'size': (tile_size, tile_size)})

    spritesheet_selector_surf = pygame.Surface((side_bar_size, 99))
    spritesheet_selector_surf.fill((20, 35, 40))
    pygame.draw.rect(spritesheet_selector_surf, (32, 50, 60), pygame.Rect(-1, -1, spritesheet_selector_surf.get_width() + 1, spritesheet_selector_surf.get_height() + 1), 1)
    for i, spritesheet in enumerate(spritesheet_keys):
        spritesheet_r = pygame.Rect(0, 1 + i * 9 - spritesheet_scroll, spritesheet_selector_surf.get_width(), 9)
        offset_x = 0
        if spritesheet_r.collidepoint((mx, my)):
            if click:
                selected_spritesheet = spritesheet
                spritesheet_img_scroll = 0
                selected_tile = None
            offset_x = 2
        font.render(spritesheet, spritesheet_selector_surf, (2 + offset_x, 1 + i * 9 - spritesheet_scroll))
    display.blit(spritesheet_selector_surf, (0, 0))

    tile_selector_surf = pygame.Surface((spritesheet_selector_surf.get_width(), display_size[1] - spritesheet_selector_surf.get_height()))
    tile_selector_surf.fill((20, 35, 40))

    if mx < spritesheet_selector_surf.get_width():
        if not spritesheet_selector_surf.get_rect().collidepoint((mx, my)):
            hovering_spritesheet_images = True

    if selected_spritesheet:
        y_pos = 0
        x_pos = 0
        for y, row in enumerate(spritesheets[selected_spritesheet]):
            tallest_img = 0
            for x, img in enumerate(row):
                offset_y = 0
                img_r = img.get_rect()
                img_r.x = 2 + x_pos - spritesheet_img_scroll
                img_r.y = 3 + y_pos + spritesheet_selector_surf.get_height() - spritesheet_img_scroll_y
                if img_r.collidepoint((mx, my)):
                    if click:
                        selected_tile = [selected_spritesheet, y, x]
                    offset_y = -2
                tile_selector_surf.blit(img, (2 + x_pos - spritesheet_img_scroll, 3 + y_pos + offset_y - spritesheet_img_scroll_y))
                x_pos += img.get_width() + 1
                tallest_img = max(tallest_img, img.get_height())
            y_pos += tallest_img + 3
            x_pos = 0

    pygame.draw.line(tile_selector_surf, (32, 50, 60), (tile_selector_surf.get_width() - 1, 0), (tile_selector_surf.get_width() - 1, tile_selector_surf.get_height() - 1))
    display.blit(tile_selector_surf, (0, spritesheet_selector_surf.get_height()))

    if spritesheet_selector_surf.get_rect().collidepoint((mx, my)):
        hovering_spritesheet_list = True

    if selected_spritesheet:
        status_str = selected_spritesheet
        if selected_tile:
            status_str += ', ' + str(selected_tile[1]) + ', ' + str(selected_tile[2])
            display.blit(spritesheet_loader.get_img(spritesheets, selected_tile), (spritesheet_selector_surf.get_width() + 4, 30))
        font.render(status_str, display, (spritesheet_selector_surf.get_width() + 4, 2))

    font.render('placement_mode: ' + str(placement_mode), display, (spritesheet_selector_surf.get_width() + 100, 2))
    layer_text = 'layer: ' + str(current_layer)
    font.render(layer_text, display, (display.get_width() - font.width(layer_text) - 2, 2))
    font.render(custom_text, display, (spritesheet_selector_surf.get_width() + 2, 12))
    font.render(str(int(round(mx / display_scale + scroll[0] - 0.5, 0))) + ', ' + str(int(round(my / display_scale + scroll[1] - 0.5, 0))), display, (spritesheet_selector_surf.get_width() + 2, 22))

    if typing_mode:
        text_surf = pygame.Surface((200, 50))
        text_surf.fill((20, 35, 40))
        display.blit(text_surf, (display_size[0] / 2 - text_surf.get_width() / 2, display_size[1] / 2 - text_surf.get_height() / 2))
        font.render(custom_text, display, (display.get_width() / 2 - font.width(custom_text) / 2, display_size[1] / 2 - 3))

    # Buttons ------------------------------------------------ #
    click = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False
            if event.button == 3:
                right_clicking = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
                clicking = True
            if event.button == 3:
                right_clicking = True
            if hovering_spritesheet_list:
                if event.button == 4:
                    spritesheet_scroll -= 9
                if event.button == 5:
                    spritesheet_scroll += 9
            elif hovering_spritesheet_images:
                if shift:
                    if event.button == 5:
                        spritesheet_img_scroll -= 14
                        spritesheet_img_scroll = max(0, spritesheet_img_scroll)
                    if event.button == 4:
                        spritesheet_img_scroll += 14
                else:
                    if event.button == 4:
                        spritesheet_img_scroll_y -= 14
                        spritesheet_img_scroll_y = max(0, spritesheet_img_scroll_y)
                    if event.button == 5:
                        spritesheet_img_scroll_y += 14
            else:
                if event.button == 4:
                    current_layer += 1
                if event.button == 5:
                    current_layer -= 1
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_RETURN:
                typing_mode = not typing_mode
            if not typing_mode:
                if event.key == K_c:
                    pyperclip.copy(id_text)
                if event.key == K_i:
                    root = Tk()
                    root.withdraw()
                    filename = filedialog.askopenfilename(initialdir = "",title = "Select Map",filetypes = (("json files","*.json"),("all files","*.*")))
                    if filename != '':
                        level_map.load_map(filename)
                if event.key == K_o:
                    level_map.write_map('save.json')
                if (not ctrl) and (not shift):
                    if event.key == K_w:
                        up = True
                    if event.key == K_s:
                        down = True
                    if event.key == K_d:
                        right = True
                    if event.key == K_a:
                        left = True
                if event.key == K_e:
                    if current_selection[0] == None:
                        current_selection = [(mx + scroll[0], my + scroll[1]), None]
                    elif current_selection[1] == None:
                        current_selection[1] = (mx + scroll[0], my + scroll[1])
                if event.key == K_l:
                    layer_opacity = not layer_opacity
                if event.key == K_g:
                    if placement_mode == 'grid_tiles':
                        placement_mode = 'off_grid_tiles'
                    else:
                        placement_mode = 'grid_tiles'
                if event.key == K_f:
                    floodfill((int(round((mx + scroll[0]) / tile_size - 0.5, 0)), int(round((my + scroll[1]) / tile_size - 0.5, 0))), level_map, selected_tile, current_layer)
                if ctrl:
                    if event.key == K_a:
                        current_selection = [None, None]
                    if event.key == K_d:
                        if current_selection[1] != None:
                            delete_list = get_selection_pos_list(current_selection)
                            for tile in delete_list:
                                deleted_tile = level_map.remove_tile(tile, current_layer)
                                if deleted_tile:
                                    deleted_tiles.append(deleted_tile)
                    if event.key == K_t:
                        if current_selection[1] != None:
                            if selected_spritesheet:
                                auto_tile(current_selection, level_map, current_layer, selected_spritesheet)
            else:
                if not ctrl:
                    for char in typing_chars:
                        if event.key == ord(char):
                            if shift:
                                if char == '-':
                                    custom_text += '_'
                                else:
                                    custom_text += char.upper()
                            else:
                                custom_text += char
                if event.key == K_BACKSPACE:
                    custom_text = custom_text[:-1]
                if event.key == K_c:
                    if ctrl:
                        custom_text = ''
            if event.key == K_LSHIFT:
                shift = True
            if event.key == K_LCTRL:
                ctrl = True
        if event.type == KEYUP:
            if not typing_mode:
                if (not ctrl) and (not shift):
                    if event.key == K_w:
                        up = False
                    if event.key == K_s:
                        down = False
                    if event.key == K_d:
                        right = False
                    if event.key == K_a:
                        left = False
            if event.key == K_LSHIFT:
                shift = False
            if event.key == K_LCTRL:
                ctrl = False

    # Update ------------------------------------------------- #
    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.update()
    mainClock.tick(60)
