package be.terrasana.module.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * Stub minimal reprenant la table "admin" héritée du stage (dictionnaire de
 * données, section 5.2). À supprimer et remplacer par l'entité Admin réelle
 * du projet du stage lors de la fusion des deux bases de code — les noms de
 * champs et le mapping de table sont identiques, donc JPA se comporte pareil.
 */
@Entity
@Table(name = "admin")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Admin {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 100)
    private String username;

    @Column(nullable = false, length = 255)
    private String password;
}
