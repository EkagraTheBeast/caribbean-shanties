package dev.caribbean.shanties.mixin;

import net.minecraft.client.renderer.LevelEventHandler;
import net.minecraft.core.BlockPos;
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
        // ClientLevelMixin performs the stop once the jukebox's has_record state becomes false.
    }
}
