package dev.caribbean.shanties;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.loot.v3.LootTableEvents;
import net.minecraft.world.level.storage.loot.LootPool;
import net.minecraft.world.level.storage.loot.entries.LootItem;
import net.minecraft.world.level.storage.loot.predicates.LootItemRandomChanceCondition;

public class CaribbeanShanties implements ModInitializer {
    public static final String MOD_ID = "caribbean_shanties";
    private static final float STRUCTURE_CHEST_CHANCE = 0.02F;

    @Override
    public void onInitialize() {
        ShantyDiscs.initialize();

        LootTableEvents.MODIFY.register((key, table, source, registries) -> {
            if (key.identifier().getNamespace().equals("minecraft") && key.identifier().getPath().startsWith("chests/")) {
                table.withPool(shantyPool()
                        .when(LootItemRandomChanceCondition.randomChance(STRUCTURE_CHEST_CHANCE)));
            }
        });
    }

    private static LootPool.Builder shantyPool() {
        LootPool.Builder pool = LootPool.lootPool();
        ShantyDiscs.ALL.forEach(item -> pool.add(LootItem.lootTableItem(item)));
        return pool;
    }
}
