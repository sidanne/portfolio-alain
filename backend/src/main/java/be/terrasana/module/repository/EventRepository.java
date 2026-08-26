package be.terrasana.module.repository;

import be.terrasana.module.entity.Event;
import be.terrasana.module.entity.enums.EventStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.LocalDateTime;
import java.util.List;

public interface EventRepository extends JpaRepository<Event, Long> {

    // Section 3.4 : liste des événements à venir, triée par date
    List<Event> findByEventDateAfterOrderByEventDateAsc(LocalDateTime now);

    // Section 3.3/3.7 : filtres et pagination par statut, lieu
    Page<Event> findByStatus(EventStatus status, Pageable pageable);

    Page<Event> findByLocationContainingIgnoreCase(String location, Pageable pageable);

    // RG-07 : événements dont la date est passée et qui sont encore OPEN/FULL (à faire basculer en FINISHED)
    List<Event> findByEventDateBeforeAndStatusIn(LocalDateTime now, List<EventStatus> statuses);
}
