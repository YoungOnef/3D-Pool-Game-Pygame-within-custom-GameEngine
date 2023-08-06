
import math
import random
#Environment class handles creation and updates of the particles 
class Environment:
    # setting the gravity constant, the angle and the magnitude
    gravity = (math.pi, 0.02)
    # fucntion to add differnet fucntion to the list for the particle to use
    def addFunctions(self, function_list):
        for f in function_list:
            #trying to get fucntion from the dictionary, if not found, provide default value
            (n, func) = self.function_dictionary.get(f, (-1, None))
            #adding function to the list for the particle
            if n == 1:
                self.particle_functions1.append(func)
            #adding function to the pair of the particles
            elif n == 2:
                self.particle_functions2.append(func)
            #if not founc then print error message
            else:
                print ("No function found called %s" %f)

    #function to initilize the environment
    def __init__(self, width, height):
        #setting the size
        self.width = width
        self.height = height
        # Initializing empty list to store particles
        self.particles = []
        # Setting default colour
        self.colour = (255, 255, 255)
        # Setting default mass of air particles
        self.mass_of_air = 0.2
        # Initializing empty lists for functions to be applied to single particles or pair of particles
        self.particle_functions1 = []
        self.particle_functions2 = []
        # Initializing empty lists for lines and circles
        self.lines = []
        self.circles = []
        # Initializing counter for number of particles removed from the environment
        self.particle_counter = 0
        #Dictionary to store different fucntions that can be appied to the particles
        self.function_dictionary = {
            'move': (1, lambda p: p.move()),  # Allow to move the particle
            'drag': (1, lambda p: p.addDrag()),  #allows to add drag to the particle
            'bounceWindowGame': (1, lambda p: self.bounceWindowGame(p)),  # Causes particle to bounce off walls of environment
            'bounceLines': (1, lambda p: self.bounceLines(p)),  # Causes particle to bounce off lines  
            'accelerate': (1, lambda p: p.accelerate(self.gravity)),  # Causes particle to accelerate in the direction of gravity
            'collide': (2, lambda p1, p2: collide(p1, p2)),  # Causes particles to collide with each other
        }
    # Adding lines from the start the end
    def addLine(self, start, end):
        self.lines.append((start, end))

    # adding circles
    def addCircle(self, x, y, size):
        self.circles.append((x, y, size))
    # checking if particles have collided with circles
    def checkCircleCollision(self):
        # Initializing empty list to store pocketed particles
        pocketed_balls = []
        # Iterating through each particle  
        for particle in self.particles:
            # Iterating through each circle  
            for x, y, size in self.circles:
                # Calculating distance between particle and circle
                distance = math.sqrt((particle.x - x)**2 + (particle.y - y)**2)
                # If the distance is less than the sum of the particle size and circle size then collide
                if distance < particle.size + size:
                    # Add particle to list of pocketed particles
                    # remove it from the environment
                    pocketed_balls.append(particle)
                    self.removeParticle(particle)
        # Return list of pocketed balls
        return pocketed_balls

                    
    # Function to remove a particle
    def removeParticle(self, particle):
        # Remove particle from the list of particles 
        self.particles.remove(particle)
        # Increment particle counter
        self.particle_counter += 1
    #add particles to the environment with defined boundaries

    def addParticles(self, n, x1, y1, x2, y2, **kargs):
        #iterate through specified number of particles
        for i in range(n):
            #if predefiens value is not find from kargs then generate random value for size
            size = kargs.get('size', random.randint(10,20))
            #if predefiens value is not find from kargs then generate random value for mass
            mass = kargs.get('mass', random.randint(100,2000))

            #if predefiens value is not find from kargs then generate random value for x coordinate within the boundaries
            x = kargs.get('x', random.uniform(x1 + size, x2 - size))
            #if predefiens value is not find from kargs then generate random value for y coordinate within the boundaries
            y = kargs.get('y', random.uniform(y1 + size, y2 - size))

            # Creating a new particle with the specified values
            p =  Particle((x, y), size, mass)

            #if predefiens value is not find from kargs then predefined value is used
            p.speed = kargs.get('speed', 0)
            #if predefiens value is not find from kargs then generate a random angle
            p.angle = kargs.get('angle', random.uniform(0, math.pi*2))
             #if predefiens value is not find from kargs then use default colour
            p.colour = kargs.get('colour', (0, 0, 255))
            # Calculate drag coefficient for the particle based on its size and mass
            p.drag = (p.mass/(p.mass + self.mass_of_air))**p.size

            # Add particle to the list of particles
            self.particles.append(p)

    #checking if particle is boucing off the game window
    def bounceWindowGame(self, particle):
        # Check if particle has collided with east wall (right side of screen)
        if particle.x > self.width - particle.size:
            # Decrease particle speed due to elastic collision
            particle.speed *= particle.elasticity
            # Reflect particle's angle across y-axis
            particle.x = 2*(self.width - particle.size) - particle.x
            particle.angle = -particle.angle
        # Check if particle has collided with west wall (left side of screen)
        if particle.x < particle.size:
            # Decrease particle speed due to elastic collision
            particle.speed *= particle.elasticity
            # Reflect particle's angle across y-axis
            particle.x = 2*particle.size - particle.x
            particle.angle = -particle.angle
        # Check if particle has collided with north wall (top of screen)
        if particle.y > self.height - particle.size:
            # Decrease particle speed due to elastic collision
            particle.speed *= particle.elasticity
            # Reflect particle's angle across x-axis
            particle.y = 2*(self.height - particle.size) - particle.y
            particle.angle = math.pi - particle.angle
        # Check if particle has collided with south wall (bottom of screen)
        if particle.y < particle.size:
            # Decrease particle speed due to elastic collision
            particle.speed *= particle.elasticity
            # Reflect particle's angle across x-axis
            particle.y = 2*particle.size - particle.y
            particle.angle = math.pi - particle.angle

    #checking if particle is boucing off the lines
    def bounceLines(self, particle):
        # Iterate through each line
        for start, end in self.lines:
            # Check if line is vertical
            if start[0] == end[0]:
                # Check if particle x position is within the range of the line x position
                if particle.x > start[0] - particle.size and particle.x < start[0] + particle.size:
                    # Check if particle y position is within the range of the line y position
                    if (particle.y > start[1] and particle.y < end[1]) or (particle.y > end[1] and particle.y < start[1]):
                        # Check if particle is on the same side as the line
                        if particle.x < start[0]:
                            # Move particle out of collision with line
                            particle.x = start[0] - particle.size
                        else:
                            # Move particle out of collision with line
                            particle.x = start[0] + particle.size
                        # Decrease particle speed due to elastic collision
                        particle.speed *= particle.elasticity
                        # Reflect particle angle across normal of the line
                        particle.angle = -particle.angle
            # Check if line is horizontal
            elif start[1] == end[1]:
                # Check if particle y position is within the range of the line y position
                if particle.y > start[1] - particle.size and particle.y < start[1] + particle.size:
                    # Check if particle x position is within the range of the line x position
                    if (particle.x > start[0] and particle.x < end[0]) or (particle.x > end[0] and particle.x < start[0]):
                        # Check if particle is on the same side as the line
                        if particle.y < start[1]:
                            # Move particle out of collision with line
                            particle.y = start[1] - particle.size
                        else:
                            # Move particle out of collision with line
                            particle.y = start[1] + particle.size
                        # Decrease particle speed due to elastic collision
                        particle.speed *= particle.elasticity
                        # Reflect particle angle across normal of the line
                        particle.angle = math.pi - particle.angle

    #updating the position and attributes of particles
    def update(self):
        # Iterate through each particle 
        for i, particle in enumerate(self.particles):
            # Apply functions in particle_functions1 list to the particle
            for f in self.particle_functions1:
                f(particle)
            # Iterate through other particles to check for interactions
            for particle2 in self.particles[i+1:]:
                # Apply functions in particle_functions2 list to pairs of particles
                for f in self.particle_functions2:
                    f(particle, particle2)

    #find a particle based on its coordinates
    def findParticle(self, coords):
        # Unpack coordinates
        (x, y) = coords
        # Iterate through each particle  
        for p in self.particles:
            # Calculate distance between particle and input coordinates
            distance = math.hypot(p.x-x, p.y-y)
            # If distance is less than or equal to the particle size return the particle
            if distance <= p.size:
                return p
        # If no particle is found return None
        return None


#add two vectors together
def addVectors(angle1, length1, angle2, length2):
    # Calculate x and y components of the two input vectors
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    # Calculate the length of the resulting vector
    length = math.hypot(x, y)
    # Calculate the angle of the resulting vector
    angle = 0.5 * math.pi - math.atan2(y, x)
    # Return the resulting angle and length
    return (angle, length)

#handling collisions between two particles
def collide(p1, p2):
    # Calculate relative coordinates of p1 and p2
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    # Calculate distance between points using Pythagorean theorem
    distance = math.hypot(dx, dy)
    # Check if collision has occurred by comparing distance to sum of sizes of particles
    if distance <= p1.size + p2.size:
        # Calculate collision angle using atan2 function and adjusting by adding 0.5 * pi
        angle = math.atan2(dy, dx) + 0.5 * math.pi

        # Calculate total mass of particles
        total_mass = p1.mass + p2.mass

        # Store temporary value of p1 speed
        p1_speed_temp = p1.speed
        # Calculate new angles and speeds of particles using addVectors function
        (p1.angle, p1.speed) = addVectors(p1.angle, p1.speed*(p1.mass - p2.mass)/total_mass, angle, 2*p2.speed*p2.mass/total_mass)
        (p2.angle, p2.speed) = addVectors(p2.angle, p2.speed*(p2.mass - p1.mass)/total_mass, angle+math.pi, 2*p1_speed_temp*p1.mass/total_mass)

        # Reduce speed due to elasticity
        p1.speed *= p1.elasticity
        p2.speed *= p2.elasticity

        # Move particles away from each other by overlap distance
        overlap = 0.5 * (p1.size + p2.size - distance + 1)
        p1.x += math.sin(angle) * overlap
        p1.y -= math.cos(angle) * overlap
        p2.x -= math.sin(angle) * overlap
        p2.y += math.cos(angle) * overlap


#Class for the particles
class Particle:
    # Constant for drag force applied to particle
    drag = 0.999
    # Constant for elasticity of particle
    elasticity = 0.9
    
    def __init__(self, coords, size, mass):
        # Initialize x and y
        x, y = coords
        self.x = x
        self.y = y
        # Initialize size of particle
        self.size = size
        # Initialize colour of particle as blue
        self.colour = (0, 0, 255)
        # Initialize thickness of particle
        self.thickness = 3
        # Initialize speed of particle
        self.speed = 0.01
        # Initialize angle of particle
        self.angle = 0
        # Initialize mass of particle from input mass
        self.mass = mass
    
    # Method to move particle based on its angle and speed
    def move(self):
        self.x += math.sin(self.angle)*self.speed
        self.y -= math.cos(self.angle)*self.speed
    
    # Method to apply drag force to particle
    def addDrag(self):
        self.speed *= self.drag
    
    # Method to update angle and speed of particle based on mouse position
    def mouseMove(self, x, y):
        # Calculate relative x and y coordinates of mouse position
        dx = x - self.x
        dy = y - self.y
        # Calculate relative speed and angle based on mouse position
        self.angle = 0.5*math.pi + math.atan2(dy, dx)
        self.speed = math.hypot(dx, dy) * 0.1 
    
    # Method to accelerate particle based on input acceleration vector
    def accelerate(self, vector):
        # Calculate new angle and speed using addVectors function
        (self.angle, self.speed) = addVectors(self.angle, self.speed, vector[0], vector[1])
