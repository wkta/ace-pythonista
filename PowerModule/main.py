import my_engi

# test
print(my_engi.REG_CONSTANT)

print('  keydown code =', my_engi.pygame.KEYDOWN)
print('  userevent code =', my_engi.pygame.USEREVENT)

print()
print('i init pygame')
my_engi.pygame.init()
print('i poll events')
print(my_engi.pygame.event.get())

print('---')
print(my_engi.plugin.BADASS_MAGIC_CONST)
print(my_engi.plugin.add(997, 3))

print('---')
print(my_engi.easymod.pi)

print('---')
print(my_engi.mathh.matrices.new_matrix)
my_engi.pygame.quit()

