import pygame
import random
import math
import time

WIDTH, HEIGHT = 800, 560
FPS = 60
BG = (30, 35, 25)


class Zombie:
    SPEED = 1.5

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = (60, 140, 60)
        self.hp = 3
        self.wobble = random.uniform(0, 6.28)
        self.frame = 0

    def update(self, player_pos):
        px, py = player_pos
        cx, cy = self.rect.center
        dx, dy = px - cx, py - cy
        dist = (dx**2 + dy**2)**0.5

        if dist:
            self.rect.x += int(dx / dist * self.SPEED)
            self.rect.y += int(dy / dist * self.SPEED)

        self.frame += 1

    def hit(self, damage=1):
        self.hp -= damage
        return self.hp <= 0

    def draw(self, screen):
        wobble_y = int(math.sin(self.frame * 0.2) * 3)
        draw_rect = self.rect.move(0, wobble_y)
        pygame.draw.rect(
            screen, self.color, draw_rect, border_radius=5
        )

        for ex in [draw_rect.x + 6, draw_rect.x + 18]:
            pygame.draw.circle(
                screen, (200, 40, 40),
                (ex, draw_rect.y + 10), 4
            )


def spawn_zombie(width, height, player_rect, margin=120, avoid_rects=None):
    avoid_rects = avoid_rects or []

    while True:
        x = random.randint(0, width - 30)
        y = random.randint(0, height - 30)
        rect = pygame.Rect(x, y, 30, 30)

        clear_of_player = not rect.colliderect(
            player_rect.inflate(margin, margin)
        )
        clear_of_obstacles = all(
            not rect.colliderect(obstacle) for obstacle in avoid_rects
        )

        if clear_of_player and clear_of_obstacles:
            return Zombie(x, y)


class ExplosiveBarrel:
    WIDTH = 28
    HEIGHT = 34
    EXPLOSION_RADIUS = 100
    EXPLOSION_DAMAGE = 3

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)
        self.active = True

    def draw(self, screen):
        if not self.active:
            return

        # Red-brown body, dark bands, and a yellow warning mark.
        pygame.draw.rect(
            screen, (150, 55, 35), self.rect, border_radius=5
        )
        pygame.draw.rect(
            screen, (65, 45, 35),
            (self.rect.x, self.rect.y + 7, self.rect.width, 5)
        )
        pygame.draw.rect(
            screen, (65, 45, 35),
            (self.rect.x, self.rect.y + 22, self.rect.width, 5)
        )
        pygame.draw.circle(
            screen, (245, 205, 55), self.rect.center, 6
        )
        pygame.draw.line(
            screen, (45, 35, 25),
            (self.rect.centerx, self.rect.centery - 4),
            (self.rect.centerx, self.rect.centery + 3), 2
        )
        pygame.draw.circle(
            screen, (45, 35, 25),
            (self.rect.centerx, self.rect.centery + 5), 1
        )


SPEED = 4


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.color = (60, 160, 220)
        self.bullets = []
        self.shoot_cooldown = 0

        # Player health and invincibility
        self.max_health = 3
        self.health = self.max_health
        self.invincibility_duration = 1.0
        self.last_damage_time = None

        # Initial protection at game start and after restart.
        self.game_started_at = time.time()
        self.start_grace_period = 2.0

        # Ammo and reload state
        self.magazine_capacity = 12
        self.ammo = self.magazine_capacity
        self.reload_duration = 2.0
        self.is_reloading = False
        self.reload_started_at = None

    def take_damage(self):
        now = time.time()

        # Do not damage a defeated or currently invincible player.
        if self.health <= 0 or self.is_invincible():
            return

        self.health = max(0, self.health - 1)
        self.last_damage_time = now

    def is_invincible(self):
        now = time.time()

        # Two seconds of protection at game start/restart.
        if now - self.game_started_at < self.start_grace_period:
            return True

        # One second of protection after taking damage.
        if self.last_damage_time is not None:
            return (
                now - self.last_damage_time
                < self.invincibility_duration
            )

        return False

    def start_reload(self):
        if (
            self.is_reloading
            or self.ammo >= self.magazine_capacity
        ):
            return

        self.is_reloading = True
        self.reload_started_at = time.monotonic()

    def update_reload(self):
        if (
            self.is_reloading
            and self.reload_started_at is not None
            and time.monotonic() - self.reload_started_at
            >= self.reload_duration
        ):
            self.ammo = self.magazine_capacity
            self.is_reloading = False
            self.reload_started_at = None

    def reset_ammo(self):
        self.ammo = self.magazine_capacity
        self.is_reloading = False
        self.reload_started_at = None

    def move(self, keys, width, height):
        dx = dy = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = SPEED

        self.rect.x = max(
            0, min(width - self.rect.width, self.rect.x + dx)
        )
        self.rect.y = max(
            0, min(height - self.rect.height, self.rect.y + dy)
        )

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def shoot(self, target_pos):
        # No shots while reloading or with an empty magazine.
        if self.is_reloading or self.ammo <= 0:
            return

        if self.shoot_cooldown > 0:
            return

        cx, cy = self.rect.center
        tx, ty = target_pos
        dx, dy = tx - cx, ty - cy
        dist = (dx**2 + dy**2)**0.5

        if dist == 0:
            return

        vx, vy = dx / dist * 10, dy / dist * 10
        self.bullets.append([cx - 4, cy - 4, vx, vy])
        self.ammo -= 1
        self.shoot_cooldown = 15

    def update_bullets(self, width, height):
        live = []

        for b in self.bullets:
            b[0] += b[2]
            b[1] += b[3]

            if 0 <= b[0] <= width and 0 <= b[1] <= height:
                live.append(b)

        self.bullets = live

    def draw(self, screen):
        # Blink while protected by temporary invincibility.
        if (
            not self.is_invincible()
            or int(time.time() * 10) % 2 == 0
        ):
            pygame.draw.rect(
                screen, self.color, self.rect, border_radius=6
            )

        for b in self.bullets:
            pygame.draw.circle(
                screen, (255, 220, 60),
                (int(b[0]), int(b[1])), 5
            )


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Zombie Escape")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 24)
        self.hud_font = pygame.font.SysFont("monospace", 16)
        self.big_font = pygame.font.SysFont(
            "monospace", 44, bold=True
        )
        self.reset()

    def reset(self):
        self.player = Player(WIDTH // 2, HEIGHT // 2)

        # Four fixed barrel locations, recreated on every restart.
        self.barrels = [
            ExplosiveBarrel(85, 80),
            ExplosiveBarrel(WIDTH - 115, 80),
            ExplosiveBarrel(85, HEIGHT - 115),
            ExplosiveBarrel(WIDTH - 115, HEIGHT - 115),
        ]
        barrel_rects = [barrel.rect for barrel in self.barrels]

        self.zombies = [
            spawn_zombie(
                WIDTH, HEIGHT, self.player.rect,
                avoid_rects=barrel_rects
            )
            for _ in range(4)
        ]
        self.explosion_effects = []

        self.score = 0
        self.kill_score = 0
        self.wave = 1
        self.kills = 0
        self.kills_to_next = 8
        self.game_over = False
        self.start_time = time.time()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()

            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_e
                and not self.game_over
            ):
                self.player.start_reload()

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and not self.game_over
            ):
                self.player.shoot(event.pos)

        return True

    def update(self):
        if self.game_over:
            return

        self.player.update_reload()

        # Expire short-lived visual explosion effects.
        now = time.monotonic()
        self.explosion_effects = [
            effect for effect in self.explosion_effects
            if now - effect["started_at"] < 0.3
        ]

        keys = pygame.key.get_pressed()
        self.player.move(keys, WIDTH, HEIGHT)
        self.player.update_bullets(WIDTH, HEIGHT)
        # Keep the existing elapsed-time score and add persistent kill points.
        self.score = int(time.time() - self.start_time) + self.kill_score

        # Zombie movement and player health collision.
        for z in self.zombies:
            z.update(self.player.rect.center)

            if z.rect.colliderect(self.player.rect):
                self.player.take_damage()

                if self.player.health <= 0:
                    self.game_over = True
                    break

        if self.game_over:
            return

        # Process bullet-barrel collisions first so a bullet can trigger
        # only one barrel and cannot also hit a zombie in the same frame.
        dead = []
        exploded_barrels = []

        for barrel in self.barrels[:]:
            if not barrel.active:
                continue

            for bullet in self.player.bullets[:]:
                bx, by = int(bullet[0]), int(bullet[1])

                if barrel.rect.collidepoint(bx, by):
                    if bullet in self.player.bullets:
                        self.player.bullets.remove(bullet)

                    barrel.active = False
                    exploded_barrels.append(barrel)
                    break

        # Remove barrels after collision iteration, then apply each blast once.
        for barrel in exploded_barrels:
            if barrel in self.barrels:
                self.barrels.remove(barrel)
            self._explode_barrel(barrel, dead)

        # Bullet-zombie collisions. Skip zombies already defeated by a blast.
        for z in self.zombies[:]:
            if z in dead:
                continue

            for bullet in self.player.bullets[:]:
                bx, by = int(bullet[0]), int(bullet[1])

                if z.rect.collidepoint(bx, by):
                    if z.hit() and z not in dead:
                        dead.append(z)

                    if bullet in self.player.bullets:
                        self.player.bullets.remove(bullet)
                    break

        # Remove defeated zombies and award points exactly once per zombie.
        for z in dead:
            if z in self.zombies:
                self.zombies.remove(z)
                self.kills += 1
                self.kill_score += 10
                self.score += 10

        # Existing wave progression.
        if self.kills >= self.kills_to_next:
            self.kills = 0
            self.wave += 1
            self.kills_to_next = 8 + self.wave * 2

            for _ in range(self.wave + 3):
                self.zombies.append(
                    spawn_zombie(
                        WIDTH, HEIGHT, self.player.rect,
                        avoid_rects=[barrel.rect for barrel in self.barrels]
                    )
                )

    def _explode_barrel(self, barrel, dead):
        center = barrel.rect.center
        radius = barrel.EXPLOSION_RADIUS
        radius_squared = radius * radius

        self.explosion_effects.append({
            "center": center,
            "radius": radius,
            "started_at": time.monotonic(),
        })

        # Use squared distance to avoid a square root for every zombie.
        for zombie in self.zombies:
            if zombie in dead:
                continue

            zx, zy = zombie.rect.center
            dx = zx - center[0]
            dy = zy - center[1]

            if dx * dx + dy * dy <= radius_squared:
                if zombie.hit(barrel.EXPLOSION_DAMAGE):
                    dead.append(zombie)

    def draw(self):
        self.screen.fill(BG)

        for x in range(0, WIDTH, 60):
            pygame.draw.line(
                self.screen, (40, 45, 35),
                (x, 0), (x, HEIGHT), 1
            )

        for y in range(0, HEIGHT, 60):
            pygame.draw.line(
                self.screen, (40, 45, 35),
                (0, y), (WIDTH, y), 1
            )

        for barrel in self.barrels:
            barrel.draw(self.screen)

        # Brief orange blast ring for visual feedback after a barrel explodes.
        now = time.monotonic()
        for effect in self.explosion_effects:
            elapsed = now - effect["started_at"]
            progress = min(1.0, elapsed / 0.3)
            current_radius = max(4, int(effect["radius"] * progress))
            pygame.draw.circle(
                self.screen, (255, 125, 35),
                effect["center"], current_radius, 4
            )
            pygame.draw.circle(
                self.screen, (255, 220, 90),
                effect["center"], max(2, current_radius // 2), 2
            )

        for z in self.zombies:
            z.draw(self.screen)

        self.player.draw(self.screen)

        hud_bg = pygame.Rect(0, 0, WIDTH, 40)
        pygame.draw.rect(self.screen, (15, 20, 15), hud_bg)

        hud = self.hud_font.render(
            f"HP: {self.player.health}/{self.player.max_health}  "
            f"AMMO: {self.player.ammo}/{self.player.magazine_capacity}  "
            f"{'RELOADING' if self.player.is_reloading else ''}  "
            f"Wave: {self.wave}  Score: {self.score}  "
            f"Kills: {self.kills}/{self.kills_to_next}",
            True, (160, 220, 120)
        )
        self.screen.blit(hud, (8, 8))

        if self.game_over:
            overlay = pygame.Surface(
                (WIDTH, HEIGHT), pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))

            message = self.big_font.render(
                "DEVOURED!", True, (180, 40, 40)
            )
            stats = self.font.render(
                f"Wave {self.wave} | Score {self.score} | Press R",
                True, (200, 200, 200)
            )

            self.screen.blit(
                message,
                (
                    WIDTH // 2 - message.get_width() // 2,
                    HEIGHT // 2 - 40
                )
            )
            self.screen.blit(
                stats,
                (
                    WIDTH // 2 - stats.get_width() // 2,
                    HEIGHT // 2 + 20
                )
            )

        pygame.display.flip()

    def run(self):
        running = True

        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    engine = GameEngine()
    engine.run()
