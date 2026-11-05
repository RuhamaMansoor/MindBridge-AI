
"""
MindBridge AI - Additional Safety Translations

Spanish and German predefined safety responses.

IMPORTANT:
These are draft localizations. They require
independent native-language and clinical safety
review before production activation.
"""

EXTRA_SAFETY_MESSAGES = {
    "es": {
        "crisis": (
            "Me preocupa tu seguridad inmediata. "
            "Comunícate ahora con los servicios de emergencia "
            "locales o acude al servicio de urgencias más cercano. "
            "Si puedes hacerlo de forma segura, aléjate de "
            "cualquier objeto con el que pudieras hacerte daño. "
            "Pide a una persona de confianza que se quede contigo "
            "y te ayude a conseguir asistencia urgente. "
            "¿Estás en un lugar seguro en este momento?"
        ),
        
            "crisis_ongoing": (
            "Me preocupa tu seguridad porque has dicho "
            "que todavía no estás a salvo. "
            "Llama ahora a los servicios de emergencia locales "
            "y explícales que necesitas ayuda inmediata. "
            "Si puedes hacerlo de forma segura, aléjate de "
            "cualquier lugar peligroso o de objetos con los "
            "que pudieras hacerte daño. "
            "Contacta con alguien de confianza y pídele "
            "que venga y permanezca contigo. "
            "No tienes que afrontar esta situación a solas."
        ),
        
        
        "clarification": (
            "Gracias por contarme cómo te sientes. "
            "Me preocupa tu seguridad y quiero tomar "
            "en serio lo que estás viviendo. "
            "Si crees que podrías hacerte daño, "
            "por favor, no te quedes a solas. "
            "Llama ahora a alguien de confianza y "
            "pídele que vaya a acompañarte o que "
            "permanezca contigo. "
            "Si puedes hacerlo de forma segura, "
            "aléjate de cualquier objeto o situación "
            "con la que pudieras hacerte daño. "
            "Si estás en peligro inmediato, llama "
            "ahora a los servicios de emergencia "
            "locales o acude a urgencias. "
            "¿Crees que podrías hacerte daño "
            "en este momento?"
        ),

        "followup": (
            "Gracias por hablar conmigo con sinceridad. "
            "¿Estás pensando en actuar según esos pensamientos "
            "ahora mismo, o has preparado algún plan? "
            "Si crees que podrías actuar, comunícate "
            "inmediatamente con los servicios de emergencia "
            "y pide a una persona de confianza que se quede contigo."
        ),
        "fallback": (
            "En este momento no puedo evaluar tu situación "
            "de manera fiable. Si estás en peligro inmediato, "
            "comunícate con los servicios de emergencia locales "
            "o acude al servicio de urgencias más cercano. "
            "También puedes buscar apoyo de una persona de "
            "confianza o de un profesional de salud mental cualificado."
        ),
        "escalation": (
            "Gracias por seguir hablando conmigo. "
            "Sigo preocupado por tu seguridad y no quiero "
            "repetirte las mismas preguntas. "
            "Busca apoyo de un profesional de salud mental "
            "cualificado o de una persona de confianza. "
            "Si existe el riesgo inmediato de que te hagas "
            "daño o dañes a otra persona, comunícate con "
            "los servicios de emergencia locales o acude "
            "inmediatamente al servicio de urgencias más cercano. "
            "Puedes seguir hablando conmigo, pero no sustituyo "
            "la atención profesional ni los servicios de emergencia."
        ),
        "service_unavailable": (
            "MindBridge AI está teniendo dificultades técnicas "
            "para responder en este momento. "
            "Inténtalo de nuevo dentro de poco. "
            "Si estás en peligro inmediato, comunícate con "
            "los servicios de emergencia locales o acude "
            "al servicio de urgencias más cercano."
        ),
    },
    "de": {
        "crisis": (
            "Ich mache mir Sorgen um Ihre unmittelbare Sicherheit. "
            "Kontaktieren Sie bitte jetzt den örtlichen Notruf "
            "oder suchen Sie die nächste Notaufnahme auf. "
            "Wenn es gefahrlos möglich ist, entfernen Sie sich "
            "von Gegenständen, mit denen Sie sich verletzen könnten. "
            "Bitten Sie eine vertraute Person, bei Ihnen zu bleiben "
            "und Ihnen dabei zu helfen, sofort Unterstützung zu bekommen. "
            "Sind Sie gerade an einem sicheren Ort?"
        ),
        
            "crisis_ongoing": (
            "Ich mache mir weiterhin Sorgen um Ihre Sicherheit, "
            "weil Sie gesagt haben, dass Sie noch nicht sicher sind. "
            "Bitte rufen Sie jetzt den örtlichen Notruf an "
            "und teilen Sie mit, dass Sie sofort Hilfe benötigen. "
            "Wenn es gefahrlos möglich ist, entfernen Sie sich "
            "von gefährlichen Orten oder Gegenständen, "
            "mit denen Sie sich verletzen könnten. "
            "Kontaktieren Sie eine vertraute Person und bitten "
            "Sie sie, zu Ihnen zu kommen und bei Ihnen zu bleiben. "
            "Sie müssen diese Situation nicht allein bewältigen."
        ),

        
        "clarification": (
            "Danke, dass Sie mir mitgeteilt haben, "
            "wie es Ihnen geht. "
            "Ich nehme Ihre Situation ernst und "
            "mache mir Sorgen um Ihre Sicherheit. "
            "Wenn Sie befürchten, sich selbst "
            "etwas anzutun, bleiben Sie bitte "
            "nicht allein. "
            "Rufen Sie jetzt eine vertraute Person "
            "an und bitten Sie sie, zu Ihnen "
            "zu kommen oder bei Ihnen zu bleiben. "
            "Wenn es gefahrlos möglich ist, "
            "entfernen Sie sich von Gegenständen "
            "oder Situationen, mit denen Sie "
            "sich verletzen könnten. "
            "Wenn Sie in unmittelbarer Gefahr sind, "
            "rufen Sie jetzt den örtlichen Notruf "
            "an oder suchen Sie eine Notaufnahme auf. "
            "Glauben Sie, dass Sie sich im Moment "
            "etwas antun könnten?"
        ),

        "followup": (
            "Vielen Dank für Ihre Offenheit. "
            "Denken Sie gerade daran, diese Gedanken in die Tat "
            "umzusetzen, oder haben Sie einen konkreten Plan? "
            "Wenn Sie befürchten, entsprechend zu handeln, "
            "kontaktieren Sie bitte sofort den Notruf und "
            "bitten Sie eine vertraute Person, bei Ihnen zu bleiben."
        ),
        "fallback": (
            "Ich kann Ihre Situation derzeit nicht zuverlässig "
            "einschätzen. Wenn Sie in unmittelbarer Gefahr sind, "
            "kontaktieren Sie bitte den örtlichen Notruf oder "
            "suchen Sie die nächste Notaufnahme auf. "
            "Sie können sich auch an eine vertraute Person "
            "oder eine qualifizierte psychologische beziehungsweise "
            "psychiatrische Fachkraft wenden."
        ),
        "escalation": (
            "Vielen Dank, dass Sie weiter mit mir sprechen. "
            "Ich mache mir weiterhin Sorgen um Ihre Sicherheit "
            "und möchte nicht immer dieselben Fragen wiederholen. "
            "Bitte wenden Sie sich an eine qualifizierte "
            "psychologische oder psychiatrische Fachkraft "
            "oder an eine vertraute Person. "
            "Wenn die unmittelbare Gefahr besteht, dass Sie "
            "sich selbst oder jemand anderem Schaden zufügen, "
            "kontaktieren Sie bitte sofort den örtlichen Notruf "
            "oder suchen Sie die nächste Notaufnahme auf. "
            "Sie können weiter mit mir sprechen, aber ich "
            "ersetze keine professionelle oder notfallmedizinische Hilfe."
        ),
        "service_unavailable": (
            "MindBridge AI hat derzeit technische Schwierigkeiten "
            "und kann nicht antworten. "
            "Bitte versuchen Sie es in Kürze erneut. "
            "Wenn Sie in unmittelbarer Gefahr sind, "
            "kontaktieren Sie bitte den örtlichen Notruf "
            "oder suchen Sie die nächste Notaufnahme auf."
        ),
    },
}
