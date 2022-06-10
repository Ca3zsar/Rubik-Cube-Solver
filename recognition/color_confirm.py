import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


colors_rgb = {
    0 : (255, 0, 0),
    1 : (0, 0, 255),
    2 : (255, 255, 255),
    3 : (0, 255, 0),
    4 : (255, 255, 0),
    5 : (255, 128, 0)
}

res = (600,720)

background_color = (64, 64, 64)
font_color = (255, 255, 255)

down_square_size = 50

down_left_offset = 100
between_offset = 20

up_line_height = 60

rubik_cube_size = 50
rubik_cube_offset = 90
rubik_in_between = 5
faces_in_between = 100
faces_in_between_vertical = 15

title_section = 20

def save_colors(colors):
    with open("cube.txt", "w") as file:
        file.write(",".join(map(str, colors)))

def load_colors():
    with open("cube.txt", "r") as file:
        cube_string = file.read()
    cube_string = cube_string.split(",")
    numbers = list(map(int, cube_string))
    return numbers

def main():
    colors = load_colors()

    pygame.init()
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption('Rubik\'s Cube Visualizer')

    width = screen.get_width()
    height = screen.get_height()

    title_font = pygame.font.SysFont('Corbel', 35)
    smallfont = pygame.font.SysFont('Corbel',15)

    title_text = title_font.render("Are the colors right?", True, font_color)
    title_rect = title_text.get_rect(center=(width/2, 40))

    save_text = smallfont.render("Save", True, font_color)
    exit_text = smallfont.render("Save & Exit", True, font_color)
    
    save_button = pygame.Rect(width//2, (height - 130)//2, 50, 25)
    save_button.center = (width//2, (height - 130)//2)
    save_rect = save_text.get_rect(center=save_button.center)

    exit_button = pygame.Rect(width//2, (height - 130)//2 + 30, 70, 25)
    exit_button.center = (width//2, (height - 130)//2 + 30)
    exit_rect = exit_text.get_rect(center=exit_button.center)

    texts = [
        smallfont.render('UP FACE' , True , font_color),
        smallfont.render('LEFT FACE' , True , font_color),
        smallfont.render('FRONT FACE' , True , font_color),
        smallfont.render('RIGHT FACE' , True , font_color),
        smallfont.render('BACK FACE' , True , font_color),
        smallfont.render('DOWN FACE' , True , font_color)
    ]

    texts_rect = [
        texts[0].get_rect(center=(rubik_cube_offset ,up_line_height + 10)),
        texts[1].get_rect(center=(width - rubik_cube_offset ,up_line_height + 10)),
        texts[2].get_rect(center=(rubik_cube_offset ,up_line_height + 10 + 180 + faces_in_between_vertical)),
        texts[3].get_rect(center=(width - rubik_cube_offset ,up_line_height + 10 + 180 + faces_in_between_vertical)),
        texts[4].get_rect(center=(rubik_cube_offset ,up_line_height + 10 + 360 + 2*faces_in_between_vertical)),
        texts[5].get_rect(center=(width - rubik_cube_offset ,up_line_height + 10 + 360 + 2*faces_in_between_vertical))
    ]

    cubies_rect = []
    for i in range(6):
        row = i // 2
        col = i % 2
        up_corner_pos = (rubik_cube_offset + col * faces_in_between + col * (3*rubik_cube_size + 2 * rubik_in_between), 
                        (row+1) * title_section + up_line_height + row * faces_in_between_vertical + row * (3*rubik_cube_size + 2 * rubik_in_between))

        for j in range(9):
            cubie_row = j // 3
            cubie_col = j % 3
            cubie_pos = (
                up_corner_pos[0] + cubie_col * (rubik_cube_size +rubik_in_between),
                up_corner_pos[1] + cubie_row * (rubik_cube_size + rubik_in_between)
            )
            rect = pygame.Rect(cubie_pos[0], cubie_pos[1], rubik_cube_size, rubik_cube_size)
            cubies_rect.append(rect)
    
    color_changer_rect = []
    for i in range(6):
        rect = pygame.Rect(down_left_offset + i * rubik_cube_size + i * between_offset, height - down_square_size - 10, down_square_size, down_square_size)
        color_changer_rect.append(rect)

    selected = None
    selected_coords = None

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                save_colors(colors)
                exit()
                
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mouse = ev.pos

                # Check what face is clicked
                for index, cubie in enumerate(cubies_rect):
                    if cubie.collidepoint(mouse):
                        selected = index
                        selected_coords = pygame.Rect(cubie.x-3, cubie.y-3, rubik_cube_size+6, rubik_cube_size+6)
                        break
                
                for index, color_changer in enumerate(color_changer_rect):
                    if color_changer.collidepoint(mouse) and selected is not None:
                        colors[selected] = index
                        selected = None
                        selected_coords = None
                        break
                
                if save_button.collidepoint(mouse):
                    save_colors(colors)

                if exit_button.collidepoint(mouse):
                    save_colors(colors)
                    pygame.quit()
                    exit()

        screen.fill(background_color)
        
        screen.blit(title_text , title_rect)

        pygame.draw.rect(screen, (0, 102, 204), save_button)
        screen.blit(save_text, save_rect)

        pygame.draw.rect(screen, (0, 102, 204), exit_button)
        screen.blit(exit_text, exit_rect)

        pygame.draw.line(screen, font_color, (0, 60), (width, 60))
        pygame.draw.line(screen, font_color, (0, height-70), (width, height-70))

        if selected_coords is not None:
            pygame.draw.rect(screen, (0,0,0), selected_coords)

        for i in range(6):
            screen.blit(texts[i], texts_rect[i])

        for index, cubie in enumerate(color_changer_rect):
            pygame.draw.rect(screen, colors_rgb[index], cubie)

        for index,cubie in enumerate(cubies_rect):
            pygame.draw.rect(screen, colors_rgb[colors[index]], cubie)
            
        pygame.display.flip()


if __name__ == '__main__':
    main()