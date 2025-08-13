import random, pygame, spade, math

from pygame.math import Vector2

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

WIDTH, HEIGHT = 800, 600
NUM_BOIDS = 20
MAX_SPEED = 3
MAX_FORCE = 0.05
PERCEPTION = 50
SEPARATION = 20
NUM_OBSTACLES = 10

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

pygame.init()
font = pygame.font.SysFont(None, 26)

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = GRAY

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        txt_surf = font.render(self.text, True, BLACK)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        screen.blit(txt_surf, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Obstacle:
    def __init__(self, pos, radius=30):
        self.pos = Vector2(pos)
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), self.radius, 1)

class Boid:
    def __init__(self):
        x, y = random.uniform(0, WIDTH), random.uniform(0, HEIGHT)
        angle = random.uniform(0, math.tau)
        self.pos = Vector2(x, y)
        self.vel = Vector2(1, 0).rotate_rad(angle)
        self.acc = Vector2(0, 0)

    def update(self, boids, obstacles):
        self.acc = Vector2(0, 0)
        self.acc += self.align(boids)
        self.acc += self.cohesion(boids)
        self.acc += self.separation(boids)
        self.acc += self.avoid_obstacles(obstacles)
        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        self.pos.x %= WIDTH
        self.pos.y %= HEIGHT

    def draw(self, screen):
        if self.vel.length() == 0:
            forward = Vector2(10, 0)
        else:
            forward = self.vel.normalize() * 10
        left = forward.rotate(140)
        right = forward.rotate(-140)
        pts = [(self.pos + p) for p in (forward, left, right)]
        pygame.draw.polygon(screen, WHITE, pts, 1)

    def align(self, boids):
        steering = Vector2()
        total = 0
        for other in boids:
            if other is self: continue
            if self.pos.distance_to(other.pos) < PERCEPTION:
                steering += other.vel
                total += 1
        if total:
            steering /= total
            steering.scale_to_length(MAX_SPEED)
            steering -= self.vel
            if steering.length() > MAX_FORCE:
                steering.scale_to_length(MAX_FORCE)
        return steering

    def cohesion(self, boids):
        steering = Vector2()
        total = 0
        for other in boids:
            if other is self: continue
            if self.pos.distance_to(other.pos) < PERCEPTION:
                steering += other.pos
                total += 1
        if total:
            steering /= total
            steering = (steering - self.pos)
            steering.scale_to_length(MAX_SPEED)
            steering -= self.vel
            if steering.length() > MAX_FORCE:
                steering.scale_to_length(MAX_FORCE)
        return steering

    def separation(self, boids):
        steering = Vector2()
        total = 0
        for other in boids:
            d = self.pos.distance_to(other.pos)
            if other is not self and d < SEPARATION:
                diff = (self.pos - other.pos) / d
                steering += diff
                total += 1
        if total:
            steering /= total
            steering.scale_to_length(MAX_SPEED)
            steering -= self.vel
            if steering.length() > MAX_FORCE:
                steering.scale_to_length(MAX_FORCE)
        return steering

    def avoid_obstacles(self, obstacles):
        steer = Vector2()
        for obs in obstacles:
            dist = self.pos.distance_to(obs.pos)
            if dist < obs.radius + 10:
                diff = self.pos - obs.pos
                if diff.length() > 0:
                    diff = diff.normalize() / dist
                    steer += diff
        if steer.length() > 0:
            steer.scale_to_length(MAX_SPEED)
            steer -= self.vel
            if steer.length() > MAX_FORCE * 2:
                steer.scale_to_length(MAX_FORCE * 2)
        return steer

class BoidAgent(Agent):
    class MoveBehaviour(CyclicBehaviour):
        async def run(self):
            if not pygame.get_init():
                await self.agent.stop()
                return
            if self.agent.screen is None:
                await self.agent.stop()
                return
            if self.agent.running:
                self.agent.boid.update(self.agent.flock, self.agent.obstacles)
            try:
                self.agent.screen.fill((0, 0, 0))
                for obs in self.agent.obstacles:
                    obs.draw(self.agent.screen)
                for b in self.agent.flock:
                    b.draw(self.agent.screen)
                for btn in self.agent.buttons:
                    btn.draw(self.agent.screen)
                pygame.display.flip()
            except pygame.error:
                await self.agent.stop()
            await spade.asyncio.sleep(1 / 60)

    def __init__(self, jid, password, screen, flock, obstacles, buttons):
        super().__init__(jid, password)
        self.screen = screen
        self.flock = flock
        self.boid = Boid()
        self.obstacles = obstacles
        self.running = False
        self.buttons = buttons

    async def setup(self):
        self.add_behaviour(self.MoveBehaviour())

async def stop_all_agents(agents):
    for agent in agents:
        await agent.stop()

async def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boids simulacija")

    start_button = Button(50, HEIGHT - 60, 100, 40, 'Kreni')
    stop_button = Button(170, HEIGHT - 60, 100, 40, 'Stani')
    reset_button = Button(290, HEIGHT - 60, 100, 40, 'Resetiraj')
    exit_button = Button(410, HEIGHT - 60, 100, 40, 'Izađi')
    buttons = [start_button, stop_button, reset_button, exit_button]

    obstacles = [   Obstacle((random.uniform(50, WIDTH - 50), random.uniform(50, HEIGHT - 50)), radius=15) for _ in range(NUM_OBSTACLES)]

    agent_accounts = [(f"boid{i}@localhost", "pass") for i in range(NUM_BOIDS)]
    flock = []
    agents = []

    for jid, pwd in agent_accounts:
        agent = BoidAgent(jid, pwd, screen, flock, obstacles, buttons)
        flock.append(agent.boid)
        agents.append(agent)

    for agent in agents:
        await agent.start(auto_register=True)

    simulation_active = True
    while simulation_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                simulation_active = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_button.is_clicked(pos):
                    for agent in agents:
                        agent.running = True
                elif stop_button.is_clicked(pos):
                    for agent in agents:
                        agent.running = False
                elif reset_button.is_clicked(pos):
                    for b in flock:
                        b.pos = Vector2(
                            random.uniform(0, WIDTH),
                            random.uniform(0, HEIGHT)
                        )
                        b.vel = Vector2(1, 0).rotate_rad(
                            random.uniform(0, math.tau)
                        )
                    for agent in agents:
                        agent.running = False
                elif exit_button.is_clicked(pos):
                    simulation_active = False
        await spade.asyncio.sleep(1 / 60)

    await stop_all_agents(agents)
    pygame.quit()

if __name__ == "__main__":
    try:
        spade.run(main())
    except KeyboardInterrupt:
        print("Program je prekinut.")