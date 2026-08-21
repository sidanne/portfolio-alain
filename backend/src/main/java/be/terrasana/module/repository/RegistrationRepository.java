package be.terrasana.module.repository;

import be.terrasana.module.entity.AppUser;
import be.terrasana.module.entity.Event;
import be.terrasana.module.entity.Registration;
import be.terrasana.module.entity.enums.RegistrationStatus;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface RegistrationRepository extends JpaRepository<Registration, Long> {

    // RG-08 : un bénévole ne peut s'inscrire qu'une seule fois au même événement
    boolean existsByUserAndEvent(AppUser user, Event event);

    Optional<Registration> findByUserAndEvent(AppUser user, Event event);

    // RG-12 : premier bénévole en liste d'attente (position la plus basse) à promouvoir
    List<Registration> findByEventAndStatusOrderByPositionAsc(Event event, RegistrationStatus status);

    // RG-18 : nombre de participations confirmées, pour le calcul du niveau
    long countByUserAndStatus(AppUser user, RegistrationStatus status);

    // Section 3.6 : inscrits confirmés + liste d'attente, par événement
    List<Registration> findByEvent(Event event);

    List<Registration> findByUser(AppUser user);
}
