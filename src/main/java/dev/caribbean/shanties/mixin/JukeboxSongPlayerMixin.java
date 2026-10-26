package dev.caribbean.shanties.mixin;

import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.world.item.JukeboxSongPlayer;
import net.minecraft.world.level.LevelAccessor;
import net.minecraft.world.level.block.entity.BlockEntityTypes;
import net.minecraft.world.level.block.entity.JukeboxBlockEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

/** Keeps the client from stopping jukebox audio while a disc is still inserted. */
@Mixin(JukeboxSongPlayer.class)
public abstract class JukeboxSongPlayerMixin {
    @Redirect(
            method = "stop",
            at = @At(
                    value = "INVOKE",
                    target = "Lnet/minecraft/world/level/LevelAccessor;levelEvent(ILnet/minecraft/core/BlockPos;I)V"))
    private void caribbeanShanties$onlyStopWhenDiscWasRemoved(
            LevelAccessor level, int event, BlockPos pos, int data) {
        Optional<JukeboxBlockEntity> jukebox = level.getBlockEntity(pos, BlockEntityTypes.JUKEBOX);
        if (jukebox.isEmpty() || jukebox.orElseThrow().isEmpty()) {
            level.levelEvent(event, pos, data);
        }
    }
}
