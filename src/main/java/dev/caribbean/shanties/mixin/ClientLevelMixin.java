package dev.caribbean.shanties.mixin;

import java.util.Map;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.renderer.LevelEventHandler;
import net.minecraft.client.resources.sounds.SoundInstance;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.RegistryAccess;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.JukeboxBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.dimension.DimensionType;
import net.minecraft.world.level.storage.WritableLevelData;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(ClientLevel.class)
public abstract class ClientLevelMixin extends Level {
    @Shadow @Final private LevelEventHandler levelEventHandler;

    protected ClientLevelMixin(
            WritableLevelData data,
            ResourceKey<Level> dimension,
            RegistryAccess registryAccess,
            Holder<DimensionType> dimensionType,
            boolean isClientSide,
            boolean isDebug,
            long biomeManagerSeed,
            int maxChainedNeighborUpdates) {
        super(data, dimension, registryAccess, dimensionType, isClientSide, isDebug,
                biomeManagerSeed, maxChainedNeighborUpdates);
    }

    @Inject(method = "setServerVerifiedBlockState", at = @At("TAIL"))
    private void caribbeanShanties$stopSoundWhenDiscLeavesJukebox(
            BlockPos pos, BlockState state, int flags, CallbackInfo callback) {
        Map<BlockPos, SoundInstance> playingSongs =
                ((LevelEventHandlerAccessor) levelEventHandler).caribbeanShanties$getPlayingJukeboxSongs();
        if (playingSongs.containsKey(pos)
                && (state.getBlock() != Blocks.JUKEBOX || !state.getValue(JukeboxBlock.HAS_RECORD))) {
            ((LevelEventHandlerAccessor) levelEventHandler)
                    .caribbeanShanties$stopJukeboxSongAndNotifyNearby(pos);
        }
    }
}
