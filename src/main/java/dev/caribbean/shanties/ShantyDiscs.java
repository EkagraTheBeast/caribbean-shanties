package dev.caribbean.shanties;

import java.util.ArrayList;
import java.util.List;
import net.fabricmc.fabric.api.creativetab.v1.FabricCreativeModeTab;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.JukeboxSong;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.network.chat.Component;

public final class ShantyDiscs {
    private ShantyDiscs() {}
    public static final List<Item> ALL = new ArrayList<>();
    private static final ResourceKey<CreativeModeTab> SHANTIES_TAB = ResourceKey.create(
            Registries.CREATIVE_MODE_TAB,
            Identifier.fromNamespaceAndPath(CaribbeanShanties.MOD_ID, "shanties"));
    private static final String[][] ENTRIES = {
        {"shanty_a_long_time_ago", "a_long_time_ago"},
        {"shanty_admiral_benbow", "admiral_benbow"},
        {"shanty_all_for_me_grog", "all_for_me_grog"},
        {"shanty_at_home_across_the_sea", "at_home_across_the_sea"},
        {"shanty_billy_riley", "billy_riley"},
        {"shanty_blood_red_roses", "blood_red_roses"},
        {"shanty_blow_away_the_morning_dew", "blow_away_the_morning_dew"},
        {"shanty_blow_the_man_down", "blow_the_man_down"},
        {"shanty_bold_riley_oh", "bold_riley_oh"},
        {"shanty_bully_in_the_alley", "bully_in_the_alley"},
        {"shanty_burn_blackbeard_s_beard", "burn_blackbeard_s_beard"},
        {"shanty_captain_kidd", "captain_kidd"},
        {"shanty_captain_ward", "captain_ward"},
        {"shanty_cheerly_men", "cheerly_men"},
        {"shanty_dead_horse", "dead_horse"},
        {"shanty_derby_ram", "derby_ram"},
        {"shanty_don_t_forget_your_old_shipmates", "don_t_forget_your_old_shipmates"},
        {"shanty_donkey_riding", "donkey_riding"},
        {"shanty_down_among_the_dead_men", "down_among_the_dead_men"},
        {"shanty_drunken_sailor", "drunken_sailor"},
        {"shanty_fathom_the_bowl", "fathom_the_bowl"},
        {"shanty_fish_in_the_sea", "fish_in_the_sea"},
        {"shanty_go_to_sea_once_more", "go_to_sea_once_more"},
        {"shanty_good_morning_ladies_all", "good_morning_ladies_all"},
        {"shanty_goodbye_fare_ye_well", "goodbye_fare_ye_well"},
        {"shanty_handy_me_boys", "handy_me_boys"},
        {"shanty_haul_away", "haul_away"},
        {"shanty_hauley_hauley_ho", "hauley_hauley_ho"},
        {"shanty_heave_away_me_johnny", "heave_away_me_johnny"},
        {"shanty_henri_martin", "henri_martin"},
        {"shanty_here_s_a_health_to_the_company", "here_s_a_health_to_the_company"},
        {"shanty_hi_for_the_beggarman", "hi_for_the_beggarman"},
        {"shanty_hi_ho_come_roll_me_over", "hi_ho_come_roll_me_over"},
        {"shanty_johnny_boker", "johnny_boker"},
        {"shanty_jolly_roving_tar", "jolly_roving_tar"},
        {"shanty_katie_cruel", "katie_cruel"},
        {"shanty_leave_her_johnny", "leave_her_johnny"},
        {"shanty_little_drummer", "little_drummer"},
        {"shanty_liverpool_judies", "liverpool_judies"},
        {"shanty_lowlands_away", "lowlands_away"},
        {"shanty_maggie_lauder", "maggie_lauder"},
        {"shanty_maid_of_amsterdam", "maid_of_amsterdam"},
        {"shanty_my_bonnie_highland_lassie", "my_bonnie_highland_lassie"},
        {"shanty_new_york_girls", "new_york_girls"},
        {"shanty_one_more_day", "one_more_day"},
        {"shanty_over_the_hills_and_far_away", "over_the_hills_and_far_away"},
        {"shanty_paddy_doyle_s_boots", "paddy_doyle_s_boots"},
        {"shanty_paddy_layback", "paddy_layback"},
        {"shanty_padstow_farewell", "padstow_farewell"},
        {"shanty_patrick_spens", "patrick_spens"},
        {"shanty_pay_me_the_money_down", "pay_me_the_money_down"},
        {"shanty_randy_dandy_oh", "randy_dandy_oh"},
        {"shanty_reuben_renzo", "reuben_renzo"},
        {"shanty_rio_grande", "rio_grande"},
        {"shanty_roll_and_go", "roll_and_go"},
        {"shanty_roll_boys_roll", "roll_boys_roll"},
        {"shanty_roller_bowler", "roller_bowler"},
        {"shanty_rolling_down_to_old_maui", "rolling_down_to_old_maui"},
        {"shanty_round_the_corner_sally", "round_the_corner_sally"},
        {"shanty_running_down_to_cuba", "running_down_to_cuba"},
        {"shanty_shallow_brown", "shallow_brown"},
        {"shanty_so_early_in_the_morning", "so_early_in_the_morning"},
        {"shanty_song_of_singapura", "song_of_singapura"},
        {"shanty_spanish_ladies", "spanish_ladies"},
        {"shanty_star_of_the_county_down", "star_of_the_county_down"},
        {"shanty_stede_bonnet", "stede_bonnet"},
        {"shanty_stormalong_john", "stormalong_john"},
        {"shanty_the_bonnie_lass_o_fyvie", "the_bonnie_lass_o_fyvie"},
        {"shanty_the_coasts_of_high_barbary", "the_coasts_of_high_barbary"},
        {"shanty_the_golden_vanity", "the_golden_vanity"},
        {"shanty_the_nightingale", "the_nightingale"},
        {"shanty_the_parting_glass", "the_parting_glass"},
        {"shanty_the_sailboat_malarkey", "the_sailboat_malarkey"},
        {"shanty_the_wellerman", "the_wellerman"},
        {"shanty_the_wild_goose", "the_wild_goose"},
        {"shanty_the_worst_old_ship", "the_worst_old_ship"},
        {"shanty_trooper_and_the_maid", "trooper_and_the_maid"},
        {"shanty_way_me_susiana", "way_me_susiana"},
        {"shanty_we_be_three_poor_mariners", "we_be_three_poor_mariners"},
        {"shanty_where_am_i_to_go_m_johnnies", "where_am_i_to_go_m_johnnies"},
        {"shanty_whisky_johnny_o", "whisky_johnny_o"},
        {"shanty_william_taylor", "william_taylor"},
        {"shanty_windy_old_weather", "windy_old_weather"},
        {"shanty_ye_jacobytes", "ye_jacobytes"}
    };
    public static void initialize() {
        for (String[] entry : ENTRIES) {
            String itemPath = entry[0];
            ResourceKey<Item> itemKey = ResourceKey.create(Registries.ITEM, Identifier.fromNamespaceAndPath(CaribbeanShanties.MOD_ID, itemPath));
            Identifier soundId = Identifier.fromNamespaceAndPath(CaribbeanShanties.MOD_ID, "shanty." + entry[1]);
            Registry.register(BuiltInRegistries.SOUND_EVENT, soundId, SoundEvent.createVariableRangeEvent(soundId));
            ResourceKey<JukeboxSong> songKey = ResourceKey.create(Registries.JUKEBOX_SONG, Identifier.fromNamespaceAndPath(CaribbeanShanties.MOD_ID, entry[1]));
            Item item = Registry.register(BuiltInRegistries.ITEM, itemKey, new Item(new Item.Properties().setId(itemKey).stacksTo(1).jukeboxPlayable(songKey)));
            ALL.add(item);
        }
        Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, SHANTIES_TAB,
                FabricCreativeModeTab.builder()
                        .title(Component.translatable("itemGroup.caribbean_shanties.shanties"))
                        .icon(() -> new ItemStack(ALL.get(0)))
                        .displayItems((parameters, output) -> ALL.forEach(output::accept))
                        .build());
    }
}
