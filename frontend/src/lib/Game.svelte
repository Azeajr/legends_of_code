<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { browser } from '$app/environment';
  import type * as PhaserType from 'phaser';

  let game: PhaserType.Game | null = null;
  let gameContainer: HTMLDivElement;

  onMount(async () => {
    if (browser) {
      // Dynamically import Phaser only on the client side
      const Phaser = (await import('phaser')) as typeof PhaserType;

      // Define the game configuration with proper typings
      const config: PhaserType.Types.Core.GameConfig = {
        type: Phaser.AUTO,
        width: 800,
        height: 600,
        parent: gameContainer,
        scene: {
          preload,
          create,
          update
        }
      };

      // Initialize the Phaser game instance
      game = new Phaser.Game(config);

      // Define the preload function with the correct 'this' context
      function preload(this: PhaserType.Scene) {
        this.load.image('sky', '/sky.png');
      }

      // Define the create function with the correct 'this' context
      function create(this: PhaserType.Scene) {
        this.add.image(400, 300, 'sky');
      }

      // Define the update function with the correct 'this' context
      function update(this: PhaserType.Scene) {
        // Game logic goes here
      }
    }
  });

  // Clean up the Phaser game instance when the component is destroyed
  onDestroy(() => {
    if (game) {
      game.destroy(true);
    }
  });
</script>

<div bind:this={gameContainer}></div>

<style>
  div {
    margin: 0 auto;
  }
</style>
