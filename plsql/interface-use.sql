BEGIN
    USER_INTERFACE.insert_user(
            p_first_name => 'Kacper',
            p_last_name => 'Kowalski',
            p_role => 'CLIENT',
            p_email => 'new_kacper_test@example.com'
        );
END;

-- BEGIN
--     USER_INTERFACE.delete_user(p_user_id => 16);
-- END;
--
-- BEGIN
--     USER_INTERFACE.update_user(
--             p_user_id => 19,
--             p_first_name => 'Janek'
--         );
-- END;
