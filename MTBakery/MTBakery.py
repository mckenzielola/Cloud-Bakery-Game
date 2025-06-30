"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
import time
import random
from PIL import Image #add for collision map 
import random # for random customer spawning
from typing import Tuple
from arcade.gui import (
    UIManager,
    UITextureButton,
    UIAnchorLayout,
    UIView,
)

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
WINDOW_TITLE = "MTBakery"

TEXTURE_DOWN = 0
TEXTURE_UP = 1
TEXTURE_LEFT = 2
TEXTURE_RIGHT = 3

MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 5

def load_textures(filename):
    return [
        filename,
        filename.flip_vertically(),
        filename.flip_diagonally().flip_left_right(),
        filename.flip_diagonally()
    ]

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui = UIManager()
        anchor = self.ui.add(UIAnchorLayout(anchor_y=300, anchor_x=WINDOW_WIDTH//2))

        # loading button textures
        button_sheet = arcade.load_spritesheet("buttonsprisheet.png")
        button_list = button_sheet.get_texture_grid(size=(480,480), columns=2, count=3)

        # loading outcome sprite textures
        outcome_sheet = arcade.load_spritesheet("outcomesprisheet.png")
        outcome_list = outcome_sheet.get_texture_grid(size=(480,480), columns=2, count=3)

        # outcome sprite
        self.outcome_sprite_list = arcade.SpriteList()
        self.outcome_sprite = arcade.Sprite(outcome_list[1])
        self.outcome_sprite.center_x = 505
        self.outcome_sprite.center_y = 600
        self.outcome_sprite.scale = 0.3
        self.outcome_sprite_list.append(self.outcome_sprite)

        # creating button
        button = anchor.add(
            UITextureButton(
                texture=button_list[0],
                width=100,
                height=100,
            )
        )

        # navigate to game view after clicking button
        @button.event("on_click")
        def on_click(event):
            self.window.show_view(GameView())

    # hiding and showing menu view
    def on_show_view(self) -> None:
        self.ui.enable()

    def on_hide_view(self) -> None:
        self.ui.disable()

    # drawing elements of menu view
    def on_draw(self):
        self.clear(color=arcade.uicolor.WHITE)
        self.outcome_sprite_list.draw()
        arcade.draw_text("MTBakery", 370, 800, arcade.color.BLACK, font_size=50)
        self.ui.draw()

class WinView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui = UIManager()
        anchor = self.ui.add(UIAnchorLayout(anchor_y=300, anchor_x=WINDOW_WIDTH//2))

        # button textures
        button_sheet = arcade.load_spritesheet("buttonsprisheet.png")
        button_list = button_sheet.get_texture_grid(size=(480,480), columns=2, count=3)

        # outcome textures
        outcome_sheet = arcade.load_spritesheet("outcomesprisheet.png")
        outcome_list = outcome_sheet.get_texture_grid(size=(480,480), columns=2, count=3)

        # rendering outcome sprite
        self.outcome_sprite_list = arcade.SpriteList()
        self.outcome_sprite = arcade.Sprite(outcome_list[0])
        self.outcome_sprite.center_x = 505
        self.outcome_sprite.center_y = 600
        self.outcome_sprite.scale = 0.3
        self.outcome_sprite_list.append(self.outcome_sprite)

        # creating button
        button = anchor.add(
            UITextureButton(
                texture=button_list[1],
                width=100,
                height=100,
            )
        )

        # navigating to menu after clicking button
        @button.event("on_click")
        def on_click(event):
            self.window.show_view(MenuView())

    # hiding and showing winning view
    def on_show_view(self) -> None:
        self.ui.enable()

    def on_hide_view(self) -> None:
        self.ui.disable()

    # drawing all elements of winning view
    def on_draw(self):
        self.clear(color=arcade.uicolor.YELLOW_SUN_FLOWER)
        arcade.draw_text("You Win!", 385, 800, arcade.color.BLACK, font_size=50)
        self.outcome_sprite_list.draw()
        self.ui.draw()

class LossView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui = UIManager()
        anchor = self.ui.add(UIAnchorLayout(anchor_y=300, anchor_x=WINDOW_WIDTH//2))

        # button textures
        button_sheet = arcade.load_spritesheet("buttonsprisheet.png")
        button_list = button_sheet.get_texture_grid(size=(480,480), columns=2, count=3)

        # outcome textures
        outcome_sheet = arcade.load_spritesheet("outcomesprisheet.png")
        outcome_list = outcome_sheet.get_texture_grid(size=(480,480), columns=2, count=3)

        # outcome sprite
        self.outcome_sprite_list = arcade.SpriteList()
        self.outcome_sprite = arcade.Sprite(outcome_list[2])
        self.outcome_sprite.center_x = 505
        self.outcome_sprite.center_y = 600
        self.outcome_sprite.scale = 0.3
        self.outcome_sprite_list.append(self.outcome_sprite)

        # drawing button
        button = anchor.add(
            UITextureButton(
                texture=button_list[2],
                width=100,
                height=100,
            )
        )

        # when button is clicked, navigate to menu view
        @button.event("on_click")
        def on_click(event):
            self.window.show_view(MenuView())

    # hiding and showing loss view 
    def on_show_view(self) -> None:
        self.ui.enable()

    def on_hide_view(self) -> None:
        self.ui.disable()

    # drawing all elements of loss view
    def on_draw(self):
        self.clear(color=arcade.uicolor.BLACK)
        arcade.draw_text("You Lose...", 365, 800, arcade.color.WHITE, font_size=50)
        self.outcome_sprite_list.draw()
        self.ui.draw()

class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()

        mc_sheet = arcade.load_spritesheet("mcsprisheet.png")
        texture_list = mc_sheet.get_texture_grid(size=(480,480), columns=3, count=10)

        self.character_face_direction = TEXTURE_DOWN

        self.cur_texture = 0
        self.idle_textures = load_textures(texture_list[0])
        self.walk_textures = []
        for i in range(10):
            texture = load_textures(texture_list[i])
            self.walk_textures.append(texture)

        # If you have sprite lists, you should create them here,
        # and set them to None

    def update_animation(self, delta_time: float = 1/60):
        if (self.change_y < 0):
            self.character_face_direction = TEXTURE_DOWN
        elif (self.change_y > 0):
            self.character_face_direction = TEXTURE_UP
        elif (self.change_x < 0):
            self.character_face_direction = TEXTURE_LEFT
        elif (self.change_x > 0):
            self.character_face_direction = TEXTURE_RIGHT

        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_textures[self.character_face_direction]
            return

        self.cur_texture += 1
        if self.cur_texture > 9 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.walk_textures[frame][direction]

class Customer(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__()

        # Store animation textures
        self.cur_texture = 0
        self.idle_textures = texture_list[0] 
        self.walk_textures = []
        for i in range(10):
            texture = load_textures(texture_list[i])
            self.walk_textures.append(texture)

        self.character_face_direction = TEXTURE_DOWN

        # Set starting position near the door
        self.center_x = 999
        self.center_y = 240

        # Movement speed
        self.speed = 2

        # Target position for ordering
        self.target_x = 800
        self.target_y = 755

        # add a speech bubble attribute to customer
        self.speech_bubble = None

        # flag to indicate when customer has been served
        self.has_been_served = False  
        # flag to indicate if customer has left
        self.has_left = False
        # flag to indicate Customer has ordered
        self.has_ordered = False
        # create timer to keep track of how long customer has been waiting for order
        self.order_time = 0

        self.old_pos = (0, 0)
        # types of orders the customer can make
        self.order_names = [
            "croissant", "cake", "cookie", "donut",
            "sourdough", "coffee", "tea"
        ]
        self.order = random.choice(self.order_names)

    def update_animation(self, delta_time: float = 1/60):
        self.cur_texture += 1
        if self.cur_texture > 9 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.walk_textures[frame][direction]

    def move_toward_target(self):
        # save change in position over time for x and y
        dx = self.target_x - self.center_x
        dy = self.target_y - self.center_y

        # if the distance between the target and the customer's current position is less than 5, target met
        if abs(dx) < 5 and abs(dy) < 5:
            self.center_x = self.target_x  # stay on target
            self.center_y = self.target_y
            self.character_face_direction = TEXTURE_LEFT  # face toward counter
            self.cur_texture = 0    # set the current texture to 0 so it is idle and not moving
            self.speed = 0  # stop moving
            # keep track of the customer spawn time
            self.spawn_time = time.time()
            return True
        
        # if the change of x is greater than the change of y, set the new direction
        if abs(dx) > abs(dy):
            # if change of x is greater than 0, set texture to right, otherwise, set the left
            self.character_face_direction = TEXTURE_RIGHT if dx > 0 else TEXTURE_LEFT
        # otherwise if the change of y is greater than x, set new direction of customer
        else:
            # if change of y is greater than 0, set customer direction to face up, otherwise set direction to down
            self.character_face_direction = TEXTURE_UP if dy > 0 else TEXTURE_DOWN
            
        # otherwise, have character move toward ordering area
        if self.center_x < self.target_x:
            self.center_x += self.speed
        elif self.center_x > self.target_x:
            self.center_x -= self.speed

        if self.center_y < self.target_y:
            self.center_y += self.speed
        elif self.center_y > self.target_y:
            self.center_y -= self.speed
        
        return False

    # function for when Customer has placed their order
    def place_order(self, current_game_time):
        self.has_ordered = True
        self.order_time = current_game_time
    
    # function for order update
    def order_update(self, delta_time):
        # check if customer has ordered and customer has not left
        if self.has_ordered and not self.has_left:
                # accumulate order time with current time
                self.order_time += delta_time
                # if the order time of the customer has exceeded 15 seconds, the customer will leave
                if self.order_time >= 15:
                    # call leave
                    self.leave()

    # function for when customer leaves
    def leave(self):
        self.has_left = True
        print("Customer left!")

class SpeechBubble(arcade.Sprite):
    def __init__(self, order):
        super().__init__()

        speech_sheet = arcade.load_spritesheet("speechsprisheet.png")
        self.speech_list = speech_sheet.get_texture_grid(size=(480,480), columns=3, count=12)

        # store the order so we can reference it later
        self.order = order
        # map food orders to texture indices
        self.order_textures = {
            "croissant": self.speech_list[9],  # Ensure these indices are correct based on the texture grid
            "cake": self.speech_list[8],
            "cookie": self.speech_list[7],
            "donut": self.speech_list[6],
            "sourdough": self.speech_list[3],
            "coffee": self.speech_list[4],
            "tea": self.speech_list[5],
        }

        # set the texture based on the order passed in
        if order in self.order_textures:
            self.texture = self.order_textures[order]

    # sets the customer's speech bubble to an angry face
    def set_angry(self):
        self.texture = self.speech_list[10]

    # sets the customer's speech bubble to an happy face
    def set_happy(self):
        self.texture = self.speech_list[11]


class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()

        # game variables, game time max
        self.total_game_time = 90.0  # seconds
        # overall game time
        self.elapsed_time = 0.0
        # flag to check if game is over
        self.game_over = False

        self.sprite_list = arcade.SpriteList()
        self.background = arcade.load_texture("Python_Game_Bg.png")

        self.score = 0
        # inventory system
        self.inventory = []  # List of sprites the player picked up
        self.inventory_spacing = 65  # Space between items in inventory bar
        self.inventory_start_x = 62  # Starting X coordinate for inventory
        self.inventory_y = 500  # Y coordinate where inventory is drawn


        #load the background to figure out collision detection based on pixels RGB values
        self.collision_bgd = Image.open("Python_Game_Bg.png")

        self.player = PlayerCharacter()
        self.sprite_list.append(self.player)
        self.player.scale = 0.2
        self.player.center_x = WINDOW_WIDTH // 4
        self.player.center_y = (WINDOW_HEIGHT * 3) // 4
        # If you have sprite lists, you should create them here,
        # and set them to None

        self.speech_list: arcade.SpriteList = arcade.SpriteList()

        # food items and placing where they go
        food_sheet = arcade.load_spritesheet("foodsprisheet.png")
        food_texture_list = food_sheet.get_texture_grid(size=(480,480), columns=3, count=7)
        self.food_list = arcade.SpriteList()
        self.donut = arcade.Sprite(food_texture_list[3])
        self.donut.center_x = (WINDOW_WIDTH * 1.122) // 2
        self.donut.center_y = (WINDOW_HEIGHT * 3.1) // 4
        self.donut.scale = 0.2

        self.croissant = arcade.Sprite(food_texture_list[0])
        self.croissant.center_x = (WINDOW_WIDTH * 0.77) // 2
        self.croissant.center_y = (WINDOW_HEIGHT * 3.42) // 4
        self.croissant.scale = 0.2

        self.cake = arcade.Sprite(food_texture_list[1])
        self.cake.center_x = (WINDOW_WIDTH * 0.05) // 2
        self.cake.center_y = (WINDOW_HEIGHT * 3.502) // 4
        self.cake.scale = 0.2

        self.cookie = arcade.Sprite(food_texture_list[2])
        self.cookie.center_x = (WINDOW_WIDTH * 1.125) // 2
        self.cookie.center_y = (WINDOW_HEIGHT * 3.43) // 4
        self.cookie.scale = 0.2

        self.sourdough = arcade.Sprite(food_texture_list[4])
        self.sourdough.center_x = (WINDOW_WIDTH * 0.771) // 2
        self.sourdough.center_y = (WINDOW_HEIGHT * 3.1) // 4
        self.sourdough.scale = 0.2   

        self.coffee = arcade.Sprite(food_texture_list[5])
        self.coffee.center_x = (WINDOW_WIDTH * 0.79) // 2
        self.coffee.center_y = (WINDOW_HEIGHT * 2.28) // 4
        self.coffee.scale = 0.2   

        self.tea = arcade.Sprite(food_texture_list[6])
        self.tea.center_x = (WINDOW_WIDTH * 0.48) // 2
        self.tea.center_y = (WINDOW_HEIGHT * 2.28) // 4
        self.tea.scale = 0.2

        self.food_list.extend([self.donut, self.croissant, self.cake, self.cookie, self.sourdough, self.coffee, self.tea])
        
        # create a dictionary for the food textures to use for add_to_inventory
        self.texture_to_order = {
            self.donut.texture: "donut",
            self.croissant.texture: "croissant",
            self.cake.texture: "cake",
            self.cookie.texture: "cookie",
            self.sourdough.texture: "sourdough",
            self.coffee.texture: "coffee",
            self.tea.texture: "tea"
        }
        # initialize a timer for when the last customer showed up
        self.time_since_last_customer = 0
        self.customer_list = arcade.SpriteList()
        #load the customers
        girl_customer_sheet = arcade.load_spritesheet("girlsprisheet.png").get_texture_grid(size=(480, 480), columns=3, count=10)
        self.girl_customer_sheet = girl_customer_sheet
        grandma_customer_sheet = arcade.load_spritesheet("grammasprisheet.png").get_texture_grid(size=(480, 480), columns=3, count=10)
        self.grandma_customer_sheet = grandma_customer_sheet
        gramps_customer_sheet = arcade.load_spritesheet("grampsprisheet.png").get_texture_grid(size=(480, 480), columns=3, count=10)
        self.grandpa_customer_sheet = gramps_customer_sheet
        boy_customer_sheet = arcade.load_spritesheet("boysprisheet.png").get_texture_grid(size=(480, 480), columns=3, count=10)
        self.boy_customer_sheet = boy_customer_sheet
        man_customer_sheet = arcade.load_spritesheet("mansprisheet.png").get_texture_grid(size=(480, 480), columns=3, count=10)
        self.man_customer_sheet = man_customer_sheet

        # available positions for customers at counter (list of tuples)
        self.order_slots = [
            (800, 675),
            (800, 740),
            (800, 814),
            (800, 882),
        ]
        # list to keep track of which counter a customer is already at
        self.order_slots_in_use = []


    # spawns a customer at random
    def spawn_customer(self):
        # using random to choose what type of customers from a list
        customer_type = random.choice(["girl", "grandma", "grandpa", "boy", "man"])

        # check the customer type
        if customer_type == "girl":
            # create a new Customer object, pass the sprite sheet 
            new_customer = Customer(self.girl_customer_sheet)
        elif customer_type == "grandma":
            #  create new Customer object, pass gramma sprite sheet
            new_customer = Customer(self.grandma_customer_sheet)
        elif customer_type == "grandpa":
            #  create new Customer object, pass grampa sprite sheet
            new_customer = Customer(self.grandpa_customer_sheet)
        elif customer_type == "boy":
            #  create new Customer object, pass boy sprite sheet
            new_customer = Customer(self.boy_customer_sheet)
        elif customer_type == "man":
            #  create new Customer object, pass man sprite sheet
            new_customer = Customer(self.man_customer_sheet)

        # set the customer scale to the same size as the player
        new_customer.scale = 0.2

        # call assign order slot to see if there is a free counter space
        slot = self.assign_order_slot()
        # if there is an available slot, assign slot to customer as target
        if slot:
            new_customer.target_x, new_customer.target_y = slot
            # add the newly created/spawned customer to the list of customers
            self.customer_list.append(new_customer)
        else:
            print("No available counter slots.")

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        arcade.draw_texture_rect(self.background, arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        self.sprite_list.draw()
        # draw the list of customers
        self.speech_list.draw()
        self.customer_list.draw()
        self.food_list.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, 475, 495, arcade.color.WHITE, 30)

        # draw the timer 
        remaining_time = max(0, int(self.total_game_time - self.elapsed_time))

        arcade.draw_text(
            f"Time Left: {remaining_time}s",
            475, 462,  
            arcade.color.RED,
            font_size=24,
            bold=True
        )
        #draw a red circle where the position of the player is (to verify pixel detection)
        #arcade.draw_circle_filled(self.player.center_x, self.player.center_y, 5, arcade.color.RED)

        # Call draw() on all your sprite lists below
        #for item in self.inventory:
            #item.draw()
        temp_list = arcade.SpriteList()
        temp_list.extend(self.inventory)
        temp_list.draw()

        


    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        # check if game is not over
        if not self.game_over:
            # accumulate elapsed time 
            self.elapsed_time += delta_time
            # check if the overall game time exceeds or is equal to the total game time
            if self.elapsed_time >= self.total_game_time:
                # set game over flag to true
                self.game_over = True
                # check player score, show game end window
                if self.score >= 50:
                    self.window.show_view(WinView())
                else:
                    self.window.show_view(LossView())
                # print debug statement
                print("Game over!!!")
        

        self.food_list.update(delta_time)

        self.speech_list.update(delta_time)

        self.sprite_list.update()
        self.sprite_list.update_animation()
        self.check_bounds() # call check bounds to see if off screen
        # passes x and y position of player to see if they are colliding with any of the background objects
        self.check_collision_with_map(int(self.player.center_x), int(self.player.center_y))

        # initialize to select a random number time delay since last customer
        self.next_customer_delay = random.randint(5, 10)
        # increment time since last customer
        self.time_since_last_customer += delta_time

        # check if the time since last customer is greater than the delay
        if self.time_since_last_customer > self.next_customer_delay:
            # spawn customer
            self.spawn_customer()

            # reset time since last customer
            self.time_since_last_customer = 0

        # update customers
        self.customer_list.update(delta_time) 

        # create a list of customers to remove once they have been served
        customers_to_remove = []

        #update the customer in the list of customers to move toward the ordering station
        for customer in self.customer_list:
            customer.move_toward_target()
            customer.update_animation(delta_time)

            # update the speech bubble position if it exists to follow customer
            if customer.speech_bubble:
                customer.speech_bubble.center_x = customer.center_x + 60
                customer.speech_bubble.center_y = customer.center_y

            if customer.move_toward_target() and customer.speech_bubble is None:
                # If the customer has an order, create a speech bubble
                if customer.order is None:  # Make sure the customer has an order
                    food_names = ["croissant", "cake", "cookie", "donut", "sourdough", "coffee", "tea"]
                    customer.order = random.choice(food_names)

                # pass the customers order to the speech bubble
                speech_bubble = SpeechBubble(customer.order)
                speech_bubble.scale = 0.2
                speech_bubble.center_x = customer.center_x + 60
                speech_bubble.center_y = customer.center_y 

                self.speech_list.append(speech_bubble)
                # assign the speech bubble as the customer's
                customer.speech_bubble = speech_bubble

                # start 15 second timer for customer
                customer.place_order(delta_time)

            # check if customer have reached the exit AND has been served
            if (customer.has_been_served == True or customer.has_left)  and abs(customer.center_x - 992) < 5 and abs(customer.center_y - 227) < 7:
                # if customer has a speech bubble, remove it
                if customer.speech_bubble in self.speech_list:
                    self.speech_list.remove(customer.speech_bubble)
                customer.speech_bubble = None 
                # add the customer to be removed to the list
                customers_to_remove.append(customer)
            
            # check if customer has ordered and has not left
            if customer.has_ordered and not customer.has_left:
                # update the order of the customer
                customer.order_update(delta_time)
                # check if customer has left is true
                if customer.has_left == True:
                    # the player gave the correct order, so serve the customer
                    customer.speech_bubble.set_angry()

                    # store the customer's counter space position
                    old_pos = (customer.center_x, customer.center_y)
                    # free the counter space, remove it from slots used
                    if old_pos in self.order_slots_in_use:
                        self.order_slots_in_use.remove(old_pos)
                        
                    # Move the customer out the door
                    customer.target_x = 992  # Set the target position outside
                    customer.target_y = 227
                    customer.speed = 1.5  # Resume moving towards the door
          
        
        # iterate through list of customers and remove them
        for customer in customers_to_remove:
            # remove customer from sprite list
            customer.remove_from_sprite_lists()
            

    def on_key_press(self, key, modifiers):
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = MOVEMENT_SPEED
        else:
            pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.DOWN or key == arcade.key.UP or key == arcade.key.S or key == arcade.key.W:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT or key == arcade.key.A or key == arcade.key.D:
            self.player.change_x = 0
        else:
            pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        #print(f"Mouse clicked at: ({x}, {y})")
        # check if user presses on items in inventory to delete item and then reposition rest
        for item in self.inventory:
            if item.collides_with_point((x, y)):
                self.inventory.remove(item)
                # reposition remaining inventory items
                for index, item in enumerate(self.inventory):
                    item.center_x = self.inventory_start_x + index * self.inventory_spacing
                    item.center_y = self.inventory_y
                return
        # checks if item in food_list has been pressed on by mouse
        for food in self.food_list:
            if food.collides_with_point((x, y)):
                # Only allow pickup if the player is close enough
                if arcade.get_distance_between_sprites(self.player, food) < 75:
                    self.add_to_inventory(food)
                    return
        
        # iterate over the list of customers to check if they have been pressed to give order to
        for customer in self.customer_list:
            # check if the click is within the customer sprite's boundaries
            if customer.collides_with_point((x, y)):
                #print(f"Clicked customer at ({customer.center_x}, {customer.center_y})")
                #print(f"Pickup: {self.pickup}, Customer order: {customer.order}")
                # give customer their order
                self.give_order_to_customer()
                return

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    # create a function to not allow player to leave the screen bounds
    def check_bounds(self):
        # if player's horizontal position is less than 0 (going left off screen), set to 0
        if self.player.center_x < 0:
            self.player.center_x = 0
        # if player's horizontal position is greater than window width (going right off screen), set to window
        if self.player.center_x > WINDOW_WIDTH:
            self.player.center_x = WINDOW_WIDTH
        # if player's vertical position is less than 0 (going out of screen on bottom)
        if self.player.center_y < 0:
            self.player.center_y = 0
        # if player's vertical position is greater than window height (going out of screen on top)
        if self.player.center_y > WINDOW_HEIGHT:
            self.player.center_y = WINDOW_HEIGHT

    # check if character is colliding with objects in the background
    def check_collision_with_map(self, x, y):
        # background y value pixels are upside down, flip the y values
        flipped_y = WINDOW_HEIGHT - y
        # Get the pixel color from the give background at the player's position
        pixel_color = self.collision_bgd.getpixel((x, flipped_y))

        # implement list of blocked colors with RGB values
        blocked_colors = [
             # counters
            (218, 138, 199, 255),
            (170, 138, 123, 255),   # wall color
            (124, 124, 124, 255),   # fridge color
            (161, 161, 161, 255),   # tray color
            (76, 52, 51, 255),      # flower pot color
            (80, 80, 80, 255)       # stove
            ]
        #print(f"{self.player.center_x} and {self.player.center_y}")
        # check if player's position pixel matches restricted colors
        # iterate through list of blocked colors
        for color in blocked_colors:
            # check if each value of the blocked colors is within 15 values of current pressed pixel
            if all(abs(pixel_color[i] - color[i]) <= 15 for i in range(3)):
                # undo movement
                self.player.center_x -= self.player.change_x
                self.player.center_y -= self.player.change_y

    # adds a given food item to player's inventory
    def add_to_inventory(self, food_sprite):
        if len(self.inventory) >= 5:
            return  # Limit inventory to 5 items

        # Create a copy of the food sprite for inventory
        item = arcade.Sprite()  # create empty sprite
        # store the texture of the food into item
        item.texture = food_sprite.texture
        # Store the order name based on texture
        item.order_name = self.texture_to_order.get(food_sprite.texture, None)

        item.scale = 0.2
        item.center_x = self.inventory_start_x + len(self.inventory) * self.inventory_spacing
        item.center_y = self.inventory_y
        self.inventory.append(item)

    # function to give customers their orders
    def give_order_to_customer(self):
        for customer in self.customer_list:
            # skip customers that don't have a speech bubble
            if customer.speech_bubble is None:
                continue
            
            # check if the player is close enough to the customer to serve the order
            if arcade.get_distance_between_sprites(self.player, customer) <= 80:
                 # iterate through the items in the players inventory to give to the customer
                for item in self.inventory:

                    # based on the texture of the food get the name of the item and compare to customer order
                    item.order_name = self.texture_to_order.get(item.texture, None)
                    # check if the player is holding the correct food that matches with order
                    if hasattr(item, "order_name") and item.order_name == customer.order:
                        # remove item that was given to customer from player's inventory
                        self.inventory.remove(item)

                        # reposition remaining inventory
                        for index, item in enumerate(self.inventory):
                            item.center_x = self.inventory_start_x + index * self.inventory_spacing
                            item.center_y = self.inventory_y

                        # set the customer's speech bubble to happy
                        customer.speech_bubble.set_happy()
                        customer.has_been_served = True # customer has been served
                                            # store the customer's counter space position
                        old_pos = (customer.center_x, customer.center_y)
                        # free the counter space, remove it from slots used
                        if old_pos in self.order_slots_in_use:
                            self.order_slots_in_use.remove(old_pos)
                        # increment score
                        self.score += 11
                        
                        # Move the customer out the door
                        customer.target_x = 992  # Set the target position outside
                        customer.target_y = 227
                        customer.speed = 1.5  # Resume moving towards the door
                        break
    
    # function to assign slots
    def assign_order_slot(self):
        # iterate through list of slots
        for slot in self.order_slots:
            # if slot is not in the slots being used, add it to slots in use
            if slot not in self.order_slots_in_use:
                # slot will now be used, store in list
                self.order_slots_in_use.append(slot)
                # return designated slot
                return slot
        return None  # no slots available




def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    window.show_view(MenuView())

    # Create and setup the GameView

    # Show GameView on screen
    # Start the arcade game loop
    arcade.run()



if __name__ == "__main__":
    main()