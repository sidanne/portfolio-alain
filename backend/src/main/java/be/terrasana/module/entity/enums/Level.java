package be.terrasana.module.entity.enums;

/**
 * RG-18 : calculé automatiquement à partir du nombre de participations confirmées.
 * BRONZE (1-2), ARGENT (3-6), OR (7+).
 */
public enum Level {
    BRONZE,
    ARGENT,
    OR;

    public static Level fromConfirmedCount(long confirmedCount) {
        if (confirmedCount >= 7) return OR;
        if (confirmedCount >= 3) return ARGENT;
        return BRONZE;
    }
}
