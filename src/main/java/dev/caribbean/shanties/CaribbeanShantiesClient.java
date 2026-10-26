package dev.caribbean.shanties;

import java.util.ArrayList;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.renderer.LevelEventHandler;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.JukeboxBlock;
import net.minecraft.world.level.block.state.BlockState;
import dev.caribbean.shanties.mixin.ClientLevelAccessor;
import dev.caribbean.shanties.mixin.LevelEventHandlerAccessor;

public final class CaribbeanShantiesClient implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        ClientTickEvents.END_CLIENT_TICK.register(CaribbeanShantiesClient::stopSoundsForRemovedDiscs);
    }

    private static void stopSoundsForRemovedDiscs(Minecraft client) {
        ClientLevel level = client.level;
        if (level == null) {
            return;
        }

        LevelEventHandler handler = ((ClientLevelAccessor) level).caribbeanShanties$getLevelEventHandler();
        LevelEventHandlerAccessor songs = (LevelEventHandlerAccessor) handler;
        for (BlockPos pos : new ArrayList<>(songs.caribbeanShanties$getPlayingJukeboxSongs().keySet())) {
            BlockState state = level.getBlockState(pos);
            if (state.getBlock() != Blocks.JUKEBOX || !state.getValue(JukeboxBlock.HAS_RECORD)) {
                songs.caribbeanShanties$stopJukeboxSongAndNotifyNearby(pos);
            }
        }
    }
}
