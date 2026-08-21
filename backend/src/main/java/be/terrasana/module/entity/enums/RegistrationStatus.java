package be.terrasana.module.entity.enums;

/**
 * RG-09/RG-10 : WAITING si l'événement est complet à l'inscription,
 * CONFIRMED/REFUSED après décision explicite de l'administrateur.
 */
public enum RegistrationStatus {
    CONFIRMED,
    WAITING,
    REFUSED
}
