package be.terrasana.module.entity.enums;

/**
 * RG-06 : OPEN par défaut, FULL dès que les places sont prises,
 * FINISHED une fois la date passée, CANCELLED sur décision de l'administrateur.
 */
public enum EventStatus {
    OPEN,
    FULL,
    CANCELLED,
    FINISHED
}
