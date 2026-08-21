package be.terrasana.module.repository;

import be.terrasana.module.entity.AppUser;
import be.terrasana.module.entity.Event;
import be.terrasana.module.entity.Review;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

public interface ReviewRepository extends JpaRepository<Review, Long> {

    // RG-16 : un seul avis par bénévole et par événement
    boolean existsByUserAndEvent(AppUser user, Event event);

    List<Review> findByEvent(Event event);

    // Section 3.5 : note moyenne affichée par événement
    @Query("select avg(r.rating) from Review r where r.event = :event")
    Double findAverageRatingByEvent(Event event);
}
