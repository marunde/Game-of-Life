import pygame
from GoL_cy_lib import helpers_cy as h
from GoL_cy_lib import constants_cy as C


def set_fps(fps):
    C.FPS = fps


def randomize_mode(setting, factor):
    C.RANDOMIZE_CELLS = setting
    C.FACTOR_OF_ALIVE_CELLS = factor


def set_max_it(iter):
    C.MAX_ITERATIONS = iter


def main():

    pygame.init()

    pygame.display.set_caption(C.CAPTION)
    icon = pygame.image.load(C.ICON)
    pygame.display.set_icon(icon)

    h.update_cell_grid_dims(C.WIN_WIDTH, C.WIN_HEIGHT, C.CELL_WIDTH)
    screen = pygame.display.set_mode((C.WIN_WIDTH, C.WIN_HEIGHT+C.WIN_STATS),
                                     pygame.RESIZABLE)

    main_font = pygame.font.SysFont('arial', 30)

    def draw_label():
        data_dict = h.get_data()
        for key in data_dict:
            test_label = main_font.render(
                f'{key} {data_dict[key][0]}', True, C.FONT_COLOUR)
            screen.blit(test_label, (200*data_dict[key][1],
                                     C.WIN_HEIGHT+30*data_dict[key][2]))

    while C.RUNNING:
        screen.fill((0, 0, 0))
        if C.MAX_ITERATIONS == C.ITERATIONS:
            C.RUN_CONTINUOUSLY = False
            C.RUNNING = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                C.RUNNING = False

            if event.type == pygame.VIDEORESIZE:
                C.WIN_WIDTH, C.WIN_HEIGHT = event.w, event.h-C.WIN_STATS
                h.update_cell_grid_dims(C.WIN_WIDTH, C.WIN_HEIGHT, C.CELL_WIDTH)
                screen = pygame.display.set_mode((C.WIN_WIDTH,
                                                  C.WIN_HEIGHT+C.WIN_STATS),
                                                 pygame.RESIZABLE)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = int(pos[0]/C.CELL_WIDTH)
                row = int(pos[1]/C.CELL_WIDTH)

                clicked_cell = C.CELL_GRID.get((column, row))

                # if a cell is clicked, switch state
                if clicked_cell:
                    clicked_cell.switch_state()
                    C.MOUSE_CLICK_CELL_STATE = clicked_cell.state
                    C.MOUSE_DRAG = True

            elif event.type == pygame.MOUSEBUTTONUP:
                C.MOUSE_DRAG = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    h.next_iteration()

                if event.key == pygame.K_DOWN:
                    if C.CELL_WIDTH-5 > 0:
                        h.update_cell_grid_dims(C.WIN_WIDTH, C.WIN_HEIGHT, C.CELL_WIDTH-5)
                        screen = pygame.display.set_mode(
                            (C.WIN_WIDTH, C.WIN_HEIGHT+C.WIN_STATS), pygame.RESIZABLE)

                if event.key == pygame.K_UP:
                    h.update_cell_grid_dims(C.WIN_WIDTH, C.WIN_HEIGHT, C.CELL_WIDTH+5)
                    screen = pygame.display.set_mode(
                        (C.WIN_WIDTH, C.WIN_HEIGHT+C.WIN_STATS), pygame.RESIZABLE)

                if event.key == pygame.K_SPACE:
                    C.RUN_CONTINUOUSLY = not C.RUN_CONTINUOUSLY

        if C.RUN_CONTINUOUSLY:
            h.next_iteration()

        if C.MOUSE_DRAG:
            h.drag(pygame.mouse.get_pos())

        h.draw_cell(screen)
        draw_label()
        pygame.time.Clock().tick(C.FPS)
        pygame.display.update()


if __name__ == '__main__':
    C.RUN_CONTINUOUSLY = True
    C.MAX_ITERATIONS = 40
    C.CELL_WIDTH = 4
    import cProfile
    cProfile.run('main()', "benchmark_profiling\\output_cy.dat")

    import pstats
    from pstats import SortKey

    with open("benchmark_profiling\\output_time_cy.txt", "w") as f:
        p = pstats.Stats("benchmark_profiling\\output_cy.dat", stream=f)
        p.sort_stats("time").print_stats()

    with open("benchmark_profiling\\output_calls_cy.txt", "w") as f:
        p = pstats.Stats("benchmark_profiling\\output_cy.dat", stream=f)
        p.sort_stats("calls").print_stats()
