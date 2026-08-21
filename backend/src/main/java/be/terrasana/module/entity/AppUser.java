package be.terrasana.module.entity;

import be.terrasana.module.entity.enums.Level;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * Bénévole — dictionnaire de données section 5.2, table "app_users".
 * Seuls firstName, lastName, email et password sont obligatoires (RG-01,
 * RG-02) : les autres champs restent facultatifs, conformément au principe
 * de minimisation des données RGPD évoqué en section 3.2.
 */
@Entity
@Table(name = "app_users")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class AppUser {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String firstName;

    @Column(nullable = false, length = 100)
    private String lastName;

    // RG-01 : identifiant de connexion, unique
    @Column(nullable = false, unique = true, length = 200)
    private String email;

    // RG-02 : haché BCrypt, jamais consultable en clair
    @Column(nullable = false, length = 255)
    private String password;

    private String phone;

    private LocalDate birthDate;

    private String gender;

    private String city;

    private String postalCode;

    @Column(columnDefinition = "TEXT")
    private String skills;

    private String availability;

    @Column(length = 5)
    private String preferredLanguage = "fr";

    @Enumerated(EnumType.STRING)
    @Column(length = 10)
    private Level level = Level.BRONZE;

    // RG-03 : désactivable sans suppression, pour conserver l'historique
    private boolean isActive = true;

    // RG-04 : jeton de réinitialisation à usage unique, valable 30 minutes
    private String resetToken;

    private LocalDateTime resetTokenExpiry;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
    }
}
