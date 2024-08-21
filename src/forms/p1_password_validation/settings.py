
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'path_to.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'path_to.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'path_to.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'path_to.password_validation.NumericPasswordValidator',
    },
]
