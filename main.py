import pygame
import sys
import random
import math

# This example demonstrates a visual simulation of a neural network training process.
# It shows a feed-forward neural network with multiple layers. The thickness and color of 
# the edges are updated over time to simulate "weights" changing. Also, text updates show 
# the current training iteration and a small "loss" value that changes over time.
#
# NOTE: This code is a conceptual visualization and not a genuine neural network training. 
# It simulates changes in weights and errors randomly to create a dynamic visual representation.

# Always handle potential errors, so we wrap initialization and main loop in try-except blocks.

# Configuration
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
FPS = 30

# Network Configuration
NUM_INPUTS = 5
NUM_HIDDEN = [6, 4]  # Two hidden layers: one with 6 neurons, another with 4 neurons
NUM_OUTPUTS = 3
LAYER_SPACING = 300
NEURON_SPACING = 80

# Colors
BG_COLOR = (30, 30, 30)
NEURON_COLOR = (200, 200, 200)
EDGE_COLOR = (100, 100, 100)
TEXT_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (0, 255, 0)

# Font sizes
FONT_SIZE = 24
SMALL_FONT_SIZE = 18

# Mock training data
# We simulate a "loss" that decreases over time and weights that vary
MAX_ITERATIONS = 2000
INITIAL_LOSS = 1.0

class NeuralNetworkVisualization:
    def __init__(self, screen, font, small_font):
        self.screen = screen
        self.font = font
        self.small_font = small_font
        self.iteration = 0
        self.loss = INITIAL_LOSS
        self.network_layers = self._generate_network_positions()
        self.weights = self._initialize_weights()
        self.max_iterations = MAX_ITERATIONS
        self.training_paused = False

    def _generate_network_positions(self):
        # Compute positions of each neuron in each layer
        # Layers: input -> hidden1 -> hidden2 -> output
        # We place input neurons on left, then hidden layers, then output on right
        layers = []
        total_layers = 2 + len(NUM_HIDDEN)  # input + output + hidden layers
        start_x = (WINDOW_WIDTH - (LAYER_SPACING * (total_layers - 1))) // 2
        # For each layer, compute y offsets
        def compute_positions(num_neurons, x):
            total_height = (num_neurons - 1) * NEURON_SPACING
            start_y = (WINDOW_HEIGHT - total_height) // 2
            return [(x, start_y + i * NEURON_SPACING) for i in range(num_neurons)]

        # Input layer
        input_positions = compute_positions(NUM_INPUTS, start_x)
        layers.append(input_positions)

        # Hidden layers
        for i, h in enumerate(NUM_HIDDEN):
            x = start_x + (i + 1) * LAYER_SPACING
            hidden_positions = compute_positions(h, x)
            layers.append(hidden_positions)

        # Output layer
        x = start_x + (len(NUM_HIDDEN) + 1) * LAYER_SPACING
        output_positions = compute_positions(NUM_OUTPUTS, x)
        layers.append(output_positions)

        return layers

    def _initialize_weights(self):
        # Initialize random weights for edges between layers
        # weights[layer][in_neuron][out_neuron] = weight_value
        # layer indexing: 0->input to hidden1, 1->hidden1 to hidden2, ...
        weights = []
        for i in range(len(self.network_layers) - 1):
            layer_in = len(self.network_layers[i])
            layer_out = len(self.network_layers[i+1])
            layer_weights = [[random.uniform(-1, 1) for _ in range(layer_out)] for _ in range(layer_in)]
            weights.append(layer_weights)
        return weights

    def update_training(self):
        # Simulate one iteration of training
        if self.training_paused:
            return

        self.iteration += 1
        if self.iteration > self.max_iterations:
            self.iteration = self.max_iterations

        # Simulate decreasing loss
        self.loss = max(0.0, INITIAL_LOSS * (1 - self.iteration / self.max_iterations))

        # Randomly adjust weights slightly to simulate training
        for layer in range(len(self.weights)):
            for i in range(len(self.weights[layer])):
                for j in range(len(self.weights[layer][i])):
                    # Small random perturbation to weights
                    change = random.uniform(-0.01, 0.01)
                    self.weights[layer][i][j] += change

    def draw(self):
        self.screen.fill(BG_COLOR)
        # Draw edges first
        for layer_idx in range(len(self.network_layers) - 1):
            for i, (x1, y1) in enumerate(self.network_layers[layer_idx]):
                for j, (x2, y2) in enumerate(self.network_layers[layer_idx + 1]):
                    w = self.weights[layer_idx][i][j]
                    # Convert weight to color/thickness
                    # Positive weight -> greener, negative weight -> redder
                    # Thickness based on absolute value
                    thickness = max(1, int(abs(w) * 5))
                    if w >= 0:
                        color = (50, 200, 50)  # Positive weights in greenish
                    else:
                        color = (200, 50, 50)  # Negative weights in reddish
                    pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), thickness)

        # Draw neurons
        for layer_idx, layer_positions in enumerate(self.network_layers):
            for (x, y) in layer_positions:
                pygame.draw.circle(self.screen, NEURON_COLOR, (x, y), 20)
                # Optionally, draw small text inside neurons, e.g. their index
                text_surface = self.small_font.render(str(layer_idx), True, BG_COLOR)
                text_rect = text_surface.get_rect(center=(x, y))
                self.screen.blit(text_surface, text_rect)

        # Draw iteration and loss text
        iteration_text = f"Iteration: {self.iteration}/{self.max_iterations}"
        loss_text = f"Loss: {self.loss:.4f}"
        iter_surf = self.font.render(iteration_text, True, TEXT_COLOR)
        loss_surf = self.font.render(loss_text, True, TEXT_COLOR)

        self.screen.blit(iter_surf, (20, 20))
        self.screen.blit(loss_surf, (20, 60))

        # Draw instructions
        instr_text = "Press SPACE to pause/resume training, ESC to quit"
        instr_surf = self.small_font.render(instr_text, True, TEXT_COLOR)
        self.screen.blit(instr_surf, (20, WINDOW_HEIGHT - 40))

        # As complexity, let's add a small animated "data point" that moves across the screen 
        # representing a training sample being processed
        # We'll base its position on iteration to animate it:
        data_x = 100 + (self.iteration % 200) * 5
        data_y = WINDOW_HEIGHT - 100
        pygame.draw.circle(self.screen, HIGHLIGHT_COLOR, (data_x, data_y), 10)
        data_text = "Data sample"
        data_surf = self.small_font.render(data_text, True, TEXT_COLOR)
        data_rect = data_surf.get_rect(center=(data_x, data_y - 25))
        self.screen.blit(data_surf, data_rect)

    def handle_key_event(self, event):
        if event.key == pygame.K_SPACE:
            self.training_paused = not self.training_paused


def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Neural Network Training Visualization")
        clock = pygame.time.Clock()

        font = pygame.font.SysFont(None, FONT_SIZE)
        small_font = pygame.font.SysFont(None, SMALL_FONT_SIZE)

        viz = NeuralNetworkVisualization(screen, font, small_font)

        running = True
        while running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                        else:
                            viz.handle_key_event(event)

                viz.update_training()
                viz.draw()
                pygame.display.flip()
                clock.tick(FPS)
            except Exception as e:
                # If there is any runtime error in the loop, we handle it and exit gracefully.
                print("Error during the main loop:", e)
                running = False
    except Exception as e:
        print("Initialization Error:", e)
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()