package be.terrasana.module.repository;

import be.terrasana.module.entity.AppUser;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface AppUserRepository extends JpaRepository<AppUser, Long> {

    // RG-01 : identifiant de connexion
    Optional<AppUser> findByEmail(String email);

    boolean existsByEmail(String email);

    // RG-04 : recherche par jeton de réinitialisation
    Optional<AppUser> findByResetToken(String resetToken);

    // Section 3.6 : filtres sur la liste des bénévoles (compétence, disponibilité, langue)
    Page<AppUser> findBySkillsContainingIgnoreCase(String skill, Pageable pageable);

    Page<AppUser> findByPreferredLanguage(String language, Pageable pageable);
}
