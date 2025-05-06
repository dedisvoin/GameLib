import sys
sys.path.append('./')

from src.app import AppWindow
from src.render import sprites, colors, base


window = AppWindow([1280, 720], "Sprites", vsync=False)
window.set_view_information_in_window()
window.set_waited_fps(1000)


sprite = sprites.load_base_sprite('examples\ex_4_sprites\img_1.png')
sprite.set_scale(10)
sprite.set_offset(sprites.OffSet.CENTER)

sprite_2 = sprites.load_base_sprite('examples\ex_4_sprites\img_2.png')
sprite_2.set_scale(1)
sprite_2.set_offset(sprites.OffSet.BOTTOM_CENTER)


animation = sprites.load_sprite_animation('examples\\ex_4_sprites\\anim*.png', 6, 0.1, True)
animation.set_scale(2)

animation_2 = animation.copy()
animation = sprites.create_outline(animation, (255, 255, 255), 2)
pos_x = 100
speed = 2



ss = sprites.load_sprite_sheet('examples\ex_4_sprites\sprite_sheet.png')
ss = list(map(lambda x: x.set_scale(10), ss))
ss[1] = sprites.create_outline(ss[1], (255, 255, 255), 1)



sprite_sheet_2 = sprites.load_sprite_sheet_grid('examples\ex_4_sprites\sprite_sheet_2.png', 4, 4)
sprite_sheet_2 = list(map(lambda x: x.set_scale(10), sprite_sheet_2))

while window.is_opened:
    sprite.rotate(3 * window.get_delta())

    window.fill(color=colors.COLOR_GRAY())

    
    sprite.base_render(window.surf, [300, 300])
    base.draw_circle(window.surf, [300, 300], 2, color=colors.COLOR_RED())

    sprite_2.base_render(window.surf, [700, 300])
    base.draw_circle(window.surf, [700, 300], 2, color=colors.COLOR_RED())

    animation.set_pos([pos_x, 500])
    animation.render(window.surf)
    animation.update()

    animation_2.set_pos([pos_x, 600])
    animation_2.render(window.surf)
    animation_2.update()

    pos_x += speed * window.get_delta()
    if pos_x > 1280 - 30 or pos_x < 40:
        animation.flip_x()
        speed *= -1


    for i in range(len(ss)):
        ss[i].base_render(window.surf, [i * 200, 100])


    sprite_sheet_2[0].base_render(window.surf, [100, 400])


    window.update()