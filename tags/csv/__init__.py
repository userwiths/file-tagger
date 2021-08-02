from .tag_manager import TagManager

def BuildConfig():
    config=Config()
    option=Option()

    config.append(
        type("Option", (Option,object), 
        {
            "name":"tags_file",
            "description":"File containing the tags"
        })

        config.append(
        type("Option", (Option,object), 
        {
            "delimiter": "delimiter that will separate the bits of data",
            "quotechar":"character that will be used instead of quotes",
            "quoting":"quoting style"
        })
    )

    return config