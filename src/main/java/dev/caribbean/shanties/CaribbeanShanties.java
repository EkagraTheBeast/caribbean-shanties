package dev.caribbean.shanties;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.loot.v3.LootTableEvents;
import net.minecraft.advancements.predicates.entity.EntityPredicate;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.storage.loot.LootContext;
import net.minecraft.world.level.storage.loot.LootPool;
import net.minecraft.world.level.storage.loot.entries.LootItem;
import net.minecraft.world.level.storage.loot.predicates.LootItemEntityPropertyCondition;
import net.minecraft.world.level.storage.loot.predicates.LootItemRandomChanceCondition;
import net.minecraft.world.level.storage.loot.LootTable;

public class CaribbeanShanties implements ModInitializer {
    public static final String MOD_ID = "caribbean_shanties";
    private static final float STRUCTURE_CHEST_CHANCE = 0.02F;
    private static final float SKELETON_CREEPER_CHANCE = 0.10F;
    private static final ResourceKey<LootTable> CREEPER_LOOT = ResourceKey.create(
            Registries.LOOT_TABLE, Identifier.withDefaultNamespace("entities/creeper"));
    private static final ResourceKey<EntityType<?>> SKELETON = ResourceKey.create(
            Registries.ENTITY_TYPE, Identifier.withDefaultNamespace("skeleton"));

    @Override
    public void onInitialize() {
        ShantyDiscs.initialize();

        LootTableEvents.MODIFY.register((key, table, source, registries) -> {
            if (CREEPER_LOOT.equals(key)) {
                table.withPool(shantyPool()
                        .when(LootItemRandomChanceCondition.randomChance(SKELETON_CREEPER_CHANCE))
                        .when(LootItemEntityPropertyCondition.hasProperties(
                                LootContext.EntityTarget.ATTACKER,
                                EntityPredicate.Builder.entity().of(
                                        registries.lookupOrThrow(Registries.ENTITY_TYPE),
                                        registries.lookupOrThrow(Registries.ENTITY_TYPE).getOrThrow(SKELETON).value()))));
                return;
            }

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
