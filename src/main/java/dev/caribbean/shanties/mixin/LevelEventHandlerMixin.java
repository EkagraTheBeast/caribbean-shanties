package dev.caribbean.shanties.mixin;

import net.minecraft.client.renderer.LevelEventHandler;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.JukeboxBlock;
import net.minecraft.world.level.block.state.BlockState;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

@Mixin(LevelEventHandler.class)
public abstract class LevelEventHandlerMixin {
    @Redirect(
            method = "levelEvent",
            at = @At(
                    value = "INVOKE",
                    target = "Lnet/minecraft/client/renderer/LevelEventHandler;stopJukeboxSongAndNotifyNearby(Lnet/minecraft/core/BlockPos;)V"))
    private void caribbeanShanties$deferJukeboxStopUntilDiscRemoval(
            LevelEventHandler handler, BlockPos pos) {
        LevelEventHandlerAccessor accessor = (LevelEventHandlerAccessor) handler;
        BlockState state = accessor.caribbeanShanties$getLevel().getBlockState(pos);
        if (state.getBlock() != Blocks.JUKEBOX || !state.getValue(JukeboxBlock.HAS_RECORD)) {
            accessor.caribbeanShanties$stopJukeboxSongAndNotifyNearby(pos);
        }
    }
}
