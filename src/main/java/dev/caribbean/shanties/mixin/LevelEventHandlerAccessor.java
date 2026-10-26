package dev.caribbean.shanties.mixin;

import java.util.Map;
import net.minecraft.client.renderer.LevelEventHandler;
import net.minecraft.client.resources.sounds.SoundInstance;
import net.minecraft.core.BlockPos;
import net.minecraft.client.multiplayer.ClientLevel;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Accessor;
import org.spongepowered.asm.mixin.gen.Invoker;

@Mixin(LevelEventHandler.class)
public interface LevelEventHandlerAccessor {
    @Accessor("level")
    ClientLevel caribbeanShanties$getLevel();

    @Accessor("playingJukeboxSongs")
    Map<BlockPos, SoundInstance> caribbeanShanties$getPlayingJukeboxSongs();

    @Invoker("stopJukeboxSongAndNotifyNearby")
    void caribbeanShanties$stopJukeboxSongAndNotifyNearby(BlockPos pos);
}
